import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type Log = {
  id: number;
  project_name: string;
  task_name: string;
  status: boolean;
  log_type: string;
  execute_type: string;
  created_at: string;
};
type LogResult = {
  total: number;
  data: Array<Log>;
};

type LogContentResult = {
  data: string;
};

export const getLogList = (params?: object) => {
  return http.request<LogResult>("get", baseUrlApi("logs"), { params });
};

export const deleteLog = (log_id: number) => {
  return http.delete(baseUrlApi(`logs/${log_id}`));
};

export const getLog = (log_id: number) => {
  return http.request<LogContentResult>(
    "get",
    baseUrlApi(`logs/${log_id}/content`)
  );
};
