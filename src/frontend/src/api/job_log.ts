import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

export type Log = {
  id: number;
  project_name?: string;
  task_name?: string;
  status: boolean;
  log_type: string;
  execute_type: string;
  created_at: string;
  content?: string;
};
type LogResult = {
  total: number;
  data: Array<Log>;
};

type LogContentResult = {
  data: string;
};

export const getLogList = (params?: object) => {
  return http.request<LogResult>("get", baseUrlApi("task_logs"), { params });
};

export const deleteLog = (log_id: number) => {
  return http.delete(baseUrlApi(`task_logs/${log_id}`));
};

export const getLog = (log_id: number) => {
  return http.request<LogContentResult>(
    "get",
    baseUrlApi(`task_logs/${log_id}/content`)
  );
};

export const getRecentlyLog = (params: object) => {
  return http.request<Log>("get", baseUrlApi("task_logs/recently"), { params });
};

export const createLog = (data: object) => {
  return http.post(baseUrlApi(`task_logs`), { data });
};
