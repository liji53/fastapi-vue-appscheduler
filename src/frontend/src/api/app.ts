import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";
import { AppCategory } from "@/api/app_category";

type App = {
  id: number;
  name: string;
  description: string;
  banner: string;
  status: string;
  category: AppCategory;
};
type AppResult = {
  total: number;
  data: Array<App>;
};

type AppConfigResult = {
  success: boolean;
  data: object;
  msg?: string;
};

/** app列表 */
export const getAppList = (params?: object) => {
  return http.request<AppResult>("get", baseUrlApi("apps"), { params });
};

// 获取已安装app的列表
export const getMyApps = () => {
  return http.request<AppResult>("get", baseUrlApi("apps/me"));
};

// 获取指定应用的默认配置
export const getAppDefaultConfig = (app_id: number) => {
  return http.request<AppConfigResult>(
    "get",
    baseUrlApi("apps/" + app_id + "/config/default")
  );
};

// 根据任务名称获取应用的配置
export const getAppConfigByTask = (app_id: number) => {
  return http.request<AppConfigResult>("get", "apps/" + app_id + "config");
};

/** 应用管理-已安装的app列表 */
export const getMyAppList = (params?: object) => {
  return http.request<AppResult>("get", "/getMyAppList", { params });
};

/** 版本日志 */
export const getReleases = () => {
  return http.request<AppResult>("get", "/releases");
};
