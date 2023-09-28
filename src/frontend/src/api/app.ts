import { http } from "@/utils/http";

type Result = {
  success: boolean;
  data: Array<any>;
  msg?: string;
};

type AppConfigResult = {
  success: boolean;
  data: object;
  msg?: string;
};

// 获取已安装app的列表
export const getMyApps = () => {
  return http.request<Result>("get", "/apps/list/me");
};

// 获取指定应用的默认配置
export const getAppDefaultConfig = (params?: object) => {
  return http.request<AppConfigResult>("get", "/apps/config/default", {
    params
  });
};

// 根据任务名称获取应用的配置
export const getAppConfigByTask = (params?: object) => {
  return http.request<AppConfigResult>("get", "/apps/config", {
    params
  });
};

/** 应用商城-app列表 */
export const getAppList = (params?: object) => {
  return http.request<Result>("get", "/getAppList", { params });
};

/** 应用管理-已安装的app列表 */
export const getMyAppList = (params?: object) => {
  return http.request<Result>("get", "/getMyAppList", { params });
};

/** 版本日志 */
export const getReleases = () => {
  return http.request<Result>("get", "/releases");
};
