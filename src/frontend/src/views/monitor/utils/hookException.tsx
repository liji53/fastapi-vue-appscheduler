import { type PaginationProps } from "@pureadmin/table";
import { reactive, ref, onMounted, toRaw, computed } from "vue";
import { message } from "@/utils/message";
import dayjs from "dayjs";
import { getLogList, deleteLog, getLog } from "@/api/log";
import { getTaskTree } from "@/api/job";

const statusTagStyle = computed(() => {
  return (status: boolean) => {
    return status
      ? {
          "--el-tag-text-color": "#389e0d",
          "--el-tag-bg-color": "#f6ffed",
          "--el-tag-border-color": "#b7eb8f"
        }
      : {
          "--el-tag-text-color": "#cf1322",
          "--el-tag-bg-color": "#fff1f0",
          "--el-tag-border-color": "#ffa39e"
        };
  };
});
const logLevelTagStyle = computed(() => {
  return (log_type: string) => {
    switch (log_type) {
      case "fatal":
        return {
          "--el-tag-text-color": "#696969",
          "--el-tag-bg-color": "#F8F8FF",
          "--el-tag-border-color": "#000000"
        };
      case "error":
        return {
          "--el-tag-text-color": "#cf1322",
          "--el-tag-bg-color": "#fff1f0",
          "--el-tag-border-color": "#ffa39e"
        };
      case "warning":
        return {
          "--el-tag-text-color": "#FF4500",
          "--el-tag-bg-color": "#FFFACD",
          "--el-tag-border-color": "#FFA500"
        };
      case "other":
        return {
          "--el-tag-text-color": "#389e0d",
          "--el-tag-bg-color": "#f6ffed",
          "--el-tag-border-color": "#b7eb8f"
        };
    }
  };
});
const logLevelText = computed(() => {
  return (log_type: string) => {
    switch (log_type) {
      case "fatal":
        return "致命";
      case "error":
        return "错误";
      case "warning":
        return "警告";
      case "other":
        return "其他";
    }
  };
});

export function useException() {
  const columns: TableColumnList = [
    {
      label: "项目名称",
      prop: "project_name",
      minWidth: 120
    },
    {
      label: "任务名称",
      prop: "task_name",
      minWidth: 120
    },
    {
      label: "执行状态",
      prop: "status",
      minWidth: 80,
      cellRenderer: ({ row }) => (
        <el-tag style={statusTagStyle.value(row.status)}>
          {row.status ? "成功" : "失败"}
        </el-tag>
      )
    },
    {
      label: "日志等级",
      prop: "log_type",
      minWidth: 120,
      cellRenderer: ({ row }) => (
        <el-tag style={logLevelTagStyle.value(row.log_type)}>
          {logLevelText.value(row.log_type)}
        </el-tag>
      )
    },
    {
      label: "执行方式",
      prop: "execute_type",
      minWidth: 120
    },
    {
      label: "运行时间",
      minWidth: 180,
      prop: "created_at",
      cellRenderer: ({ row }) => (
        <el-tag size="small">
          {dayjs(row.created_at).format("YYYY-MM-DD HH:mm:ss")}
        </el-tag>
      )
    },
    {
      label: "操作",
      fixed: "right",
      width: 200,
      slot: "operation"
    }
  ];
  const loading = ref(true);
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 10,
    currentPage: 1
  });
  const form = reactive({
    task_ids: null,
    status: "",
    log_type: "",
    page: 1,
    itemsPerPage: 10
  });
  const taskTreeProps = ref({
    value: "id",
    label: "name",
    children: "children"
  });
  const dialogVisible = ref(false);

  const logList = ref([]); // 日志列表
  const taskTree = ref([]); // 项目-任务树
  const logTxt = ref(""); // 日志内容

  function onSearch() {
    loading.value = true;
    getLogList(toRaw(form))
      .then(data => {
        logList.value = data.data;
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

  function handleDelete(row) {
    deleteLog(row.id).then(() => {
      message("您删除了一条日志", { type: "success" });
      onSearch();
    });
  }

  function openDialog(row) {
    getLog(row.id).then(response => {
      logTxt.value = response.data;
      dialogVisible.value = true;
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

  onMounted(() => {
    onSearch();
    getTaskTree().then(response => {
      taskTree.value = response.data;
    });
  });

  return {
    form,
    loading,
    columns,
    logList,
    taskTree,
    taskTreeProps,
    pagination,
    onSearch,
    resetForm,
    openDialog,
    handleDelete,
    handleSizeChange,
    handleCurrentChange,
    dialogVisible,
    logTxt
  };
}
