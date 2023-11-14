import dayjs from "dayjs";
import editForm from "../components/jobForm.vue";
import { message } from "@/utils/message";
import { getJobList, createJob, updateJob, deleteJob } from "@/api/job";
import { getMyAppTree } from "@/api/installed_app";
import { getProjectList } from "@/api/project";
import { ElMessageBox } from "element-plus";
import { addDialog } from "@/components/ReDialog";
import { type JobItemProps } from "./types";
import { type PaginationProps } from "@pureadmin/table";
import { reactive, ref, onMounted, h, computed, toRaw } from "vue";

export function useJob() {
  const form = reactive({
    name: "",
    project_id: "",
    status: "",
    page: 1,
    itemsPerPage: 10
  });
  const dataList = ref([]);
  const projects = ref([]);
  const apps = ref([]);
  const loading = ref(true);
  const formRef = ref();
  const switchLoadMap = ref({});
  const switchStyle = computed(() => {
    return {
      "--el-switch-on-color": "#6abe39",
      "--el-switch-off-color": "#e84749"
    };
  });
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 10,
    currentPage: 1
  });
  const crontabVisible = ref(false);
  const isShowCronCore = ref(true);
  const cronFormData = reactive({
    id: null,
    cron: "* * * * *"
  });

  const columns: TableColumnList = [
    {
      label: "任务编号",
      prop: "id",
      minWidth: 100
    },
    {
      label: "任务名称",
      prop: "name",
      minWidth: 120
    },
    {
      label: "项目",
      prop: "project",
      minWidth: 120
    },
    {
      label: "状态",
      minWidth: 130,
      cellRenderer: scope => (
        <el-switch
          size={scope.props.size === "small" ? "small" : "default"}
          loading={switchLoadMap.value[scope.index]?.loading}
          v-model={scope.row.status}
          active-value={true}
          inactive-value={false}
          active-text="启用"
          inactive-text="停用"
          inline-prompt
          style={switchStyle.value}
          onChange={() => onChangeStatus(scope as any)}
        />
      )
    },
    {
      label: "备注",
      prop: "remark",
      minWidth: 150
    },
    {
      label: "更新时间",
      minWidth: 180,
      prop: "updated_at",
      formatter: ({ updated_at }) =>
        dayjs(updated_at).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "操作",
      fixed: "right",
      width: 240,
      slot: "operation"
    }
  ];

  // 使能状态切换
  function onChangeStatus({ row, index }) {
    ElMessageBox.confirm(
      `确认要<strong>${
        row.status === false ? "停用" : "启用"
      }</strong><strong style='color:var(--el-color-primary)'>${
        row.name
      }</strong>吗?`,
      "系统提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        dangerouslyUseHTMLString: true,
        draggable: true
      }
    )
      .then(async () => {
        switchLoadMap.value[index] = Object.assign(
          {},
          switchLoadMap.value[index],
          {
            loading: true
          }
        );
        await updateJob(row.id, { status: row.status })
          .then(async () => {
            message(`已${row.status === false ? "停用" : "启用"}${row.name}`, {
              type: "success"
            });
          })
          .catch(() => {
            // 请求失败，恢复状态
            row.status === false ? (row.status = true) : (row.status = false);
          });
        // 加载状态恢复
        switchLoadMap.value[index] = Object.assign(
          {},
          switchLoadMap.value[index],
          {
            loading: false
          }
        );
      })
      .catch(() => {
        // 取消 恢复状态
        row.status === false ? (row.status = true) : (row.status = false);
      });
  }

  function handleRun(row) {
    console.log(row.id);
  }

  // 定时任务相关逻辑
  function handleTimer(row) {
    cronFormData.id = row["id"];
    cronFormData.cron = row["cron"];
    crontabVisible.value = true;
  }
  // const onChangeCron = val => {
  //   if (typeof val !== "string") return false;
  //   cronFormData.cron = val;
  // };
  const onCancelCron = () => {
    crontabVisible.value = false;
  };
  const onConfirmCron = async () => {
    await updateJob(cronFormData.id, { cron: cronFormData.cron });
    onSearch();
  };

  function handleConfig(row) {
    console.log(row.id);
  }

  function handleDelete(row) {
    deleteJob(row.id).then(() => {
      message(`您删除了任务-${row.name}`, { type: "success" });
      onSearch();
    });
  }

  function handleSizeChange(val: number) {
    form.page = 1;
    form.itemsPerPage = val;
    onSearch();
  }

  function handleCurrentChange(val: number) {
    form.page = val;
    onSearch();
  }

  // 表单
  function onSearch() {
    loading.value = true;
    getJobList(toRaw(form))
      .then(data => {
        dataList.value = data.data;
        pagination.total = data.total;
      })
      .finally(() => {
        loading.value = false;
      });
  }
  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  };

  function openDialog(title = "新增", row?: JobItemProps) {
    addDialog({
      title: `${title}任务`,
      props: {
        formInline: {
          id: row?.id ?? "",
          name: row?.name ?? "",
          remark: row?.remark ?? "",
          project_id: row?.project_id ?? "",
          app_id: row?.app_id ?? "",
          projects: projects,
          apps: apps
        }
      },
      width: "40%",
      draggable: true,
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as JobItemProps;
        function chores() {
          message(`您${title}了任务${curData.name}`, {
            type: "success"
          });
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
        FormRef.validate(valid => {
          if (valid) {
            // 表单规则校验通过
            if (title === "新增") {
              createJob(curData).then(() => {
                chores();
              });
            } else {
              updateJob(curData.id, curData).then(() => {
                chores();
              });
            }
          }
        });
      }
    });
  }

  onMounted(() => {
    onSearch();
    getProjectList().then(response => {
      projects.value = response.data;
    });
    getMyAppTree().then(response => {
      apps.value = response.data;
    });
  });

  return {
    form,
    loading,
    columns,
    dataList,
    projects,
    pagination,
    onSearch,
    resetForm,
    openDialog,
    handleRun,
    handleTimer,
    handleConfig,
    handleDelete,
    handleSizeChange,
    handleCurrentChange,
    crontabVisible,
    isShowCronCore,
    cronFormData,
    //onChangeCron,
    onCancelCron,
    onConfirmCron
  };
}
