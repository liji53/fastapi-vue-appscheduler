import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type Job = {
  id: number;
  name: string;
  project: string;
  project_id: number;
  app_id: number; // 指的是已安装的应用
  remark: string;
  status: boolean;
  next_at: string;
  updated_at: string;
  cron: string;
  url: string;
};
type JobResult = {
  total: number;
  data: Array<Job>;
};

type JobConfigResult = {
  data: string;
};
type TaskTree = {
  id?: number;
  name: string;
  children?: Array<TaskTree>;
};
type TaskTreeResult = {
  data: Array<TaskTree>;
};

export const getJobList = (params?: object) => {
  return http.request<JobResult>("get", baseUrlApi("tasks"), { params });
};

export const createJob = (data: object) => {
  return http.post(baseUrlApi("tasks"), { data });
};

export const updateJob = (job_id: number, data: object) => {
  return http.put(baseUrlApi(`tasks/${job_id}`), { data });
};

export const deleteJob = (job_id: number) => {
  return http.delete(baseUrlApi(`tasks/${job_id}`));
};

export const runJob = (job_id: number) => {
  return http.post(baseUrlApi(`tasks/${job_id}/run`));
};

export const getJobConfig = (job_id: number) => {
  return http.request<JobConfigResult>(
    "get",
    baseUrlApi(`tasks/${job_id}/config`)
  );
};

export const setJobConfig = (job_id: number, data: object) => {
  return http.put(baseUrlApi(`tasks/${job_id}/config`), { data });
};
// 异常监控
export const getTaskTree = () => {
  return http.request<TaskTreeResult>("get", baseUrlApi("tasks/tree"));
};
