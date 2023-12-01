import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type App = {
  id: number;
  name: string;
  url: string;
  description: string;
  banner: string;
  status: boolean;
  is_installed: boolean;
  category_id: number;
};
type AppResult = {
  total: number;
  data: Array<App>;
};

// 应用的tree形式
export type AppTree = {
  id: number;
  name: string;
  children?: Array<AppTree>;
};
export type AppTreeResult = { data: Array<AppTree> };

/** app列表 */
export const getAppList = (params?: object) => {
  return http.request<AppResult>("get", baseUrlApi("apps"), { params });
};

export const createApp = (data: object) => {
  return http.post(baseUrlApi("apps"), { data });
};

export const updateApp = (app_id: number, data: object) => {
  return http.put(baseUrlApi(`apps/${app_id}`), { data });
};

export const deleteApp = (app_id: number) => {
  return http.delete(baseUrlApi(`apps/${app_id}`));
};

// 上传应用的图片
export const uploadPic = (app_id: number, data: object) => {
  return http.upload(baseUrlApi(`apps/${app_id}/banner`), { data });
};

// 应用配置设计 - 获取应用的tree
export const getAppTree = () => {
  return http.request<AppTreeResult>("get", baseUrlApi("apps/tree"));
};
