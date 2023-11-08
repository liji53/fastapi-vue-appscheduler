import { reactive, ref, onMounted, h } from "vue";
import { getAppCategory } from "@/api/app_category";
import type { FormRules } from "element-plus";
import {
  getAppList,
  createApp,
  updateApp,
  deleteApp,
  uploadPic
} from "@/api/app";
import { installApp } from "@/api/installed_app";
import { message } from "@/utils/message";
import { addDialog } from "@/components/ReDialog";
import croppingUpload from "../components/upload.vue";

export function useApp() {
  const loading = ref(true);
  const pagination = reactive({
    total: 0,
    pageSize: 8,
    currentPage: 1
  });
  const avatarInfo = ref();

  // 搜索表单
  const form = reactive({
    name: "",
    category_id: null,
    status: null,
    page: 1,
    itemsPerPage: 8
  });

  // 后台数据
  const categories = ref([]);
  const apps = ref([]);

  // 新增、编辑相关的dialog
  const dialogVisable = ref(false);
  const dialogTitle = ref("新增");
  const INITIAL_DATA = {
    id: null,
    name: "",
    status: true,
    url: "",
    category_id: null,
    description: ""
  };
  // 表单
  const appForm = ref({ ...INITIAL_DATA });
  // 表单rule
  const appFormRules = reactive(<FormRules>{
    name: [{ required: true, message: "应用名称为必填项", trigger: "blur" }],
    url: [
      {
        type: "url",
        required: true,
        message: "请输入合法的URL地址",
        trigger: "blur"
      }
    ]
  });

  // 搜索表单的响应
  function onSearch() {
    loading.value = true;
    getAppList(form)
      .then(response => {
        apps.value = response.data;
        pagination.total = response.total;
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

  // 分页
  const onPageSizeChange = (val: number) => {
    form.page = 1;
    form.itemsPerPage = val;
    onSearch();
  };
  const onCurrentPageChange = (val: number) => {
    form.page = val;
    onSearch();
  };

  // 点击上架, 不会保存上次编辑的内容
  const onAddApp = () => {
    dialogVisable.value = true;
    dialogTitle.value = "新增";
    appForm.value = { ...INITIAL_DATA };
  };
  // 确认 上架/编辑 应用
  const onConfirmApp = fromE1 => {
    fromE1.validate(valid => {
      if (valid) {
        if (dialogTitle.value === "新增") {
          createApp(appForm.value).then(() => {
            message(`您新增了应用${appForm.value.name}`, {
              type: "success"
            });
            dialogVisable.value = false;
            onSearch();
          });
        } else {
          updateApp(appForm.value.id, appForm.value).then(() => {
            message(`您编辑了应用${appForm.value.name}`, {
              type: "success"
            });
            dialogVisable.value = false;
            onSearch();
          });
        }
      }
    });
  };

  // 用于响应AppCard的事件
  const handleInstallApp = async (app_id: number) => {
    await installApp({ app_id: app_id });
    onSearch();
  };
  const handleRevisionApp = (app_id: number) => {
    message("暂时不支持查看应用版本", {
      type: "error"
    });
  };
  const handleEditApp = app => {
    dialogVisable.value = true;
    dialogTitle.value = "编辑";
    appForm.value = { ...app };
  };
  const handleDisableApp = async (app_id: number) => {
    await updateApp(app_id, { status: false });
    onSearch();
  };
  const handleEnableApp = async (app_id: number) => {
    await updateApp(app_id, { status: true });
    onSearch();
  };
  const handleDeleteApp = async (app_id: number) => {
    await deleteApp(app_id);
    onSearch();
  };
  const handleUploadPicApp = app => {
    addDialog({
      title: "裁剪、上传应用图片",
      width: "40%",
      draggable: true,
      closeOnClickModal: false,
      contentRenderer: () =>
        h(croppingUpload, {
          imgSrc: app.banner ?? "/default_avatar.jpeg", // 默认头像
          onCropper: info => (avatarInfo.value = info)
        }),
      beforeSure: done => {
        // 根据实际业务使用avatarInfo.value和row里的某些字段去调用上传头像接口即可
        uploadPic(app.id, avatarInfo.value).then(() => {
          message(`您上传了应用${appForm.value.name}的logo`, {
            type: "success"
          });
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        });
      }
    });
  };

  onMounted(() => {
    onSearch();
    getAppCategory().then(response => {
      categories.value = response.data;
    });
  });

  // 获取app类别 名字
  function getCategoryName(category_id: number) {
    for (const item of categories.value) {
      if (item.id === category_id) {
        return item.name;
      }
    }
  }

  return {
    form,
    loading,
    categories,
    apps,
    pagination,
    dialogVisable,
    dialogTitle,
    appForm,
    appFormRules,
    onSearch,
    resetForm,
    onPageSizeChange,
    onCurrentPageChange,
    onAddApp,
    onConfirmApp,
    handleInstallApp,
    handleRevisionApp,
    handleEditApp,
    handleDisableApp,
    handleEnableApp,
    handleDeleteApp,
    handleUploadPicApp,
    getCategoryName
  };
}
