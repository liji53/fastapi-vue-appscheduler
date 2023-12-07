import dayjs from "dayjs";
import editForm from "../components/projectForm.vue";
import { message } from "@/utils/message";
import {
  getProjectList,
  createProject,
  updateProject,
  deleteProject
} from "@/api/project";
import { addDialog } from "@/components/ReDialog";
import { type ProjectItemProps } from "./types";
import { type PaginationProps } from "@pureadmin/table";
import { reactive, ref, onMounted, h, computed } from "vue";

const faildCountTagStyle = computed(() => {
  return (faild_count: number) => {
    return faild_count
      ? {
          "--el-tag-text-color": "#cf1322",
          "--el-tag-bg-color": "#fff1f0",
          "--el-tag-border-color": "#ffa39e"
        }
      : {
          "--el-tag-text-color": "#389e0d",
          "--el-tag-bg-color": "#f6ffed",
          "--el-tag-border-color": "#b7eb8f"
        };
  };
});

export function useProject() {
  const dataList = ref([]);
  const loading = ref(true);
  const formRef = ref();
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 10,
    currentPage: 1
  });
  const columns: TableColumnList = [
    {
      label: "项目名称",
      prop: "name",
      minWidth: 120
    },
    {
      label: "任务数量",
      prop: "task_count",
      minWidth: 120,
      cellRenderer: ({ row }) => <el-tag>{row.task_count}</el-tag>
    },
    {
      label: "已上线的任务",
      prop: "online_count",
      minWidth: 120
    },
    {
      label: "运行失败的任务",
      prop: "failed_count",
      minWidth: 120,
      cellRenderer: ({ row }) => (
        <el-tag style={faildCountTagStyle.value(row.failed_count)}>
          {row.failed_count}
        </el-tag>
      )
    },
    {
      label: "备注",
      prop: "remark",
      minWidth: 150
    },
    {
      label: "创建时间",
      minWidth: 180,
      prop: "created_at",
      formatter: ({ created_at }) =>
        dayjs(created_at).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "操作",
      fixed: "right",
      width: 240,
      slot: "operation"
    }
  ];

  function handleDelete(row) {
    deleteProject(row.id).then(() => {
      message(`您删除了项目-${row.name}`, { type: "success" });
      onSearch();
    });
  }

  function handleSizeChange() {
    onSearch();
  }

  function handleCurrentChange() {
    onSearch();
  }

  function onSearch() {
    loading.value = true;
    getProjectList({
      page: pagination.currentPage,
      itemsPerPage: pagination.pageSize
    })
      .then(data => {
        dataList.value = data.data;
        pagination.total = data.total;
      })
      .finally(() => {
        loading.value = false;
      });
  }

  function openDialog(title = "新增", row?: ProjectItemProps) {
    addDialog({
      title: `${title}项目`,
      props: {
        formInline: {
          id: row?.id ?? "",
          name: row?.name ?? "",
          remark: row?.remark ?? ""
        }
      },
      width: "40%",
      draggable: true,
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as ProjectItemProps;
        function chores() {
          message(`您${title}了项目${curData.name}`, {
            type: "success"
          });
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
        FormRef.validate(valid => {
          if (valid) {
            // 表单规则校验通过
            if (title === "新增") {
              createProject(curData).then(() => {
                chores();
              });
            } else {
              updateProject(curData.id, curData).then(() => {
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
  });

  return {
    loading,
    columns,
    dataList,
    pagination,
    onSearch,
    openDialog,
    handleDelete,
    handleSizeChange,
    handleCurrentChange
  };
}
