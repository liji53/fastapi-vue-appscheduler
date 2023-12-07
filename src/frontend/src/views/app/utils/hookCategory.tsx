import dayjs from "dayjs";
import editForm from "../components/CategoryForm.vue";
import { message } from "@/utils/message";
import {
  type AppCategory,
  getAppCategory,
  createCategory,
  updateCategory,
  deleteCategory
} from "@/api/app_category";
import { addDialog } from "@/components/ReDialog";
import { type PaginationProps } from "@pureadmin/table";
import { reactive, ref, onMounted, h } from "vue";

export function useCategory() {
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
      label: "应用分类",
      prop: "name",
      minWidth: 120
    },
    {
      label: "应用数量",
      prop: "app_count",
      minWidth: 120,
      cellRenderer: ({ row }) => <el-tag>{row.app_count}</el-tag>
    },
    {
      label: "已安装的应用",
      prop: "installed_app_count",
      minWidth: 120
    },
    {
      label: "总安装次数",
      prop: "installed_sum_count",
      minWidth: 120
    },
    {
      label: "描述",
      prop: "description",
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
    deleteCategory(row.id).then(() => {
      message(`您删除了分类-${row.name}`, { type: "success" });
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
    getAppCategory({
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

  function openDialog(title = "新增", row?: AppCategory) {
    addDialog({
      title: `${title}分类`,
      props: {
        formInline: {
          id: row?.id ?? "",
          name: row?.name ?? "",
          description: row?.description ?? ""
        }
      },
      width: "40%",
      draggable: true,
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as AppCategory;
        function chores() {
          message(`您${title}了分类${curData.name}`, {
            type: "success"
          });
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
        FormRef.validate(valid => {
          if (valid) {
            // 表单规则校验通过
            if (title === "新增") {
              createCategory(curData).then(() => {
                chores();
              });
            } else {
              updateCategory(curData.id, curData).then(() => {
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
