import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type AppForm = {
  form: string;
};

// 应用配置设计 - 获取应用的表单
export const getAppForm = (app_id: number) => {
  return http.request<AppForm>("get", baseUrlApi(`appforms/${app_id}`));
};
// 设置应用的表单
export const setAppForm = (app_id: number, data: object) => {
  return http.put(baseUrlApi(`appforms/${app_id}`), { data });
};
