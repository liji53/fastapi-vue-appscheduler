import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type InstalledApp = {
  id: number;
  name: string;
  remark: string;
  is_online: boolean;
  category_id: number;
  version: string;
};
type AppResult = {
  total: number;
  data: Array<InstalledApp>;
};

// 安装应用的tree形式
type AppTree = {
  id: number;
  name: string;
  children?: Array<AppTree>;
};
type AppTreeResult = { data: Array<AppTree> };

// 我的应用列表
export const getMyInstallApps = (params?: object) => {
  return http.request<AppResult>("get", baseUrlApi("installed_apps"), {
    params
  });
};

/** 安装应用 */
export const installApp = (data: object) => {
  return http.post(baseUrlApi("installed_apps"), { data });
};

/** 卸载应用 */
export const uninstallApp = (app_id: number) => {
  return http.delete(baseUrlApi(`installed_apps/${app_id}`));
};

// 更新应用信息
export const updateApp = (app_id: number, data: object) => {
  return http.put(baseUrlApi(`installed_apps/${app_id}`), { data });
};

// 上传应用的图片
export const uploadPic = (app_id: number, data: object) => {
  return http.upload(baseUrlApi(`installed_apps/${app_id}/banner`), { data });
};

// 任务管理-获取已安装应用的app Tree列表
export const getMyAppTree = () => {
  return http.request<AppTreeResult>("get", baseUrlApi("installed_apps/tree"));
};
