import dayjs from "dayjs";
import editForm from "../components/jobForm.vue";
import { message } from "@/utils/message";
import { getJobList, createJob, updateJob, deleteJob } from "@/api/job";
import { getRecentlyLog, type Log } from "@/api/job_log";
import { getMyAppTree } from "@/api/installed_app";
import { getProjectList } from "@/api/project";
import { getAppForm } from "@/api/app_form";
import { ElMessageBox } from "element-plus";
import { addDialog } from "@/components/ReDialog";
import { type JobItemProps } from "./types";
import { type PaginationProps } from "@pureadmin/table";
import { reactive, ref, onMounted, h, computed, toRaw } from "vue";
import { invoke } from "@tauri-apps/api";

const nextAtStyle = computed(() => {
  return (next_at: string) => {
    return next_at == null
      ? {
          "--el-tag-text-color": "#cf1322",
          "--el-tag-bg-color": "#fff1f0",
          "--el-tag-border-color": "#ffa39e"
        }
      : {};
  };
});

export function useJob() {
  // header 表单的数据
  const form = reactive({
    name: "",
    project_id: "",
    status: "",
    page: 1,
    itemsPerPage: 10
  });
  const dataList = ref([]); // 任务列表
  const projects = ref([]); // 项目列表
  const apps = ref([]); // 安装的应用的树结构
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
  // 定时设置
  const crontabVisible = ref(false);
  const cronFormData = reactive({
    id: null,
    cron: "* * * * *"
  });
  // 任务配置
  const taskConifgVisible = ref(false);
  const taskRow = ref(); // 设置配置时记录当前任务id
  const taskConfigData = ref([]); // 任务的当前配置
  // 运行日志
  const logVisible = ref(false);
  const log = ref<Log>({
    status: false,
    id: null,
    log_type: null,
    execute_type: null,
    created_at: null
  });

  const columns: TableColumnList = [
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
      minWidth: 80,
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
      label: "下次执行时间",
      minWidth: 160,
      prop: "next_at",
      cellRenderer: ({ row }) => (
        <el-tag size="small" style={nextAtStyle.value(row.next_at)}>
          {row.next_at != null
            ? dayjs(row.next_at).format("YYYY-MM-DD HH:mm:ss")
            : "未上线"}
        </el-tag>
      )
    },
    {
      label: "更新时间",
      minWidth: 160,
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
  // 手动执行任务(异步，在通知栏中listen任务完成的事件)
  async function handleRun(row) {
    invoke("run_app", { repoUrl: row.url, taskName: row.name, taskId: row.id })
      .then(() => {
        message(`开始运行【${row.name}】`, {
          type: "success"
        });
      })
      .catch(error => {
        message(`运行【${row.name}】失败: ${error}`, {
          type: "error"
        });
      });
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
    if (cronFormData.cron != null && cronFormData.cron.trim() === "") {
      await updateJob(cronFormData.id, { cron: null });
    } else {
      await updateJob(cronFormData.id, { cron: cronFormData.cron });
    }

    message(`成功设置定时任务`, {
      type: "success"
    });
    crontabVisible.value = false;
    onSearch();
  };

  // 设置任务的配置
  function handleConfig(row) {
    getAppForm({ task_id: row.id }).then(response => {
      invoke("getconfig_app", {
        repoUrl: row.url,
        appForm: response.form === null ? "[]" : response.form,
        taskId: row.id
      })
        .then((response: string) => {
          if (response === "") {
            message(`应用【${row.name}】不需要配置`, {
              type: "warning"
            });
          } else {
            taskConfigData.value = JSON.parse(response);
            taskConifgVisible.value = true;
            taskRow.value = row;
          }
        })
        .catch(error => {
          message(`应用【${row.name}】的配置异常: ${error}`, {
            type: "error"
          });
        });
    });
  }
  function handleConfirmConfig(formRef, config) {
    formRef.validate(async valid => {
      if (valid) {
        invoke("setconfig_app", {
          repoUrl: taskRow.value.url,
          taskId: taskRow.value.id,
          config: JSON.stringify(config)
        })
          .then(() => {
            message("配置设置成功", { type: "success" });
          })
          .catch((error: string) => {
            message(error, { type: "error" });
          });
      }
    });
  }

  // 删除任务
  function handleDelete(row) {
    deleteJob(row.id).then(() => {
      message(`您删除了任务-${row.name}`, { type: "success" });
      onSearch();
    });
  }

  // 分页
  function handleSizeChange(val: number) {
    form.page = 1;
    form.itemsPerPage = val;
    onSearch();
  }
  function handleCurrentChange(val: number) {
    form.page = val;
    onSearch();
  }

  // 搜索任务列表
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

  // 新增、编辑 任务
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
  // 查看日志
  function handleLog(row) {
    getRecentlyLog({ task_id: row.id }).then((response: Log) => {
      log.value = response;
      logVisible.value = true;
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
    cronFormData,
    //onChangeCron,
    onCancelCron,
    onConfirmCron,
    taskConifgVisible,
    taskConfigData,
    handleConfirmConfig,
    logVisible,
    log,
    handleLog
  };
}
