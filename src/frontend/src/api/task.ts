import { http } from "@/utils/http";

type Result = {
  success: boolean;
  data?: [any];
};

/** 任务中心-任务列表 */
export const getTaskList = () => {
  return http.request<Result>("get", "/tasks/list");
};

export const addTask = (data?: object) => {
  return http.request<Result>("post", "/tasks", { data });
};

export const updateTask = (data?: object) => {
  return http.request<Result>("put", "/tasks", { data });
};

export const deleteTask = (data?: object) => {
  return http.request<Result>("delete", "/tasks", { data });
};
