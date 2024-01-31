import { reactive, ref, onMounted, h } from "vue";
import { getAppCategory } from "@/api/app_category";
import type { FormRules } from "element-plus";
import {
  getMyInstallApps,
  deleteInstalledApp,
  updateApp,
  uploadPic
} from "@/api/installed_app";
import { invoke } from "@tauri-apps/api";
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
    category_id: "",
    is_online: "",
    page: 1,
    itemsPerPage: 8
  });

  // 后台数据
  const categories = ref([]);
  const apps = ref([]); // 已安装的app

  // 新增、编辑相关的dialog
  const dialogVisable = ref(false);
  const dialogTitle = ref("编辑");
  const INITIAL_DATA = {
    id: null,
    name: "",
    description: ""
  };
  // 应用表单
  const appForm = ref({ ...INITIAL_DATA });
  // 表单rule
  const appFormRules = reactive(<FormRules>{
    name: [{ required: true, message: "应用名称为必填项", trigger: "blur" }]
  });
  const readme = ref("");

  // 搜索表单的响应
  async function onSearch() {
    loading.value = true;
    getMyInstallApps(form)
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

  // 确认 编辑 应用
  const onConfirmApp = fromE1 => {
    fromE1.validate(valid => {
      if (valid) {
        updateApp(appForm.value.id, appForm.value).then(() => {
          message(`您编辑了应用${appForm.value.name}`, {
            type: "success"
          });
          dialogVisable.value = false;
          onSearch();
        });
      }
    });
  };

  // 用于响应AppCard的事件
  const handleRevisionApp = (app_id: number) => {
    message(`暂时不支持查看应用${app_id}的版本`, {
      type: "error"
    });
  };
  const handleEditApp = app => {
    dialogVisable.value = true;
    dialogTitle.value = "编辑";
    appForm.value = { ...app };
  };
  const handleUninstallApp = async app => {
    // 本地安装应用
    invoke("uninstall_app", { repoUrl: app.url })
      .then(() => {
        // 删除数据库中应用的元数据
        deleteInstalledApp(app.id)
          .then(() => {
            message(`您卸载了应用${app.name}`, {
              type: "success"
            });
          })
          .finally(() => {
            onSearch();
          });
      })
      .catch((res: string) => {
        message(res, { type: "error" });
        return;
      });
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
  const handleReadmeApp = async app => {
    // 产看本地应用的readme.md
    invoke("readme_app", { repoUrl: app.url })
      .then((response: string) => {
        readme.value = response;
      })
      .catch((err: string) => {
        readme.value = "";
        message(err, { type: "error" });
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
    readme,
    onSearch,
    resetForm,
    onPageSizeChange,
    onCurrentPageChange,
    onConfirmApp,
    handleUninstallApp,
    handleRevisionApp,
    handleEditApp,
    handleUploadPicApp,
    handleReadmeApp,
    getCategoryName
  };
}
