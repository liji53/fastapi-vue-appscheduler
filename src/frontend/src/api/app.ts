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
