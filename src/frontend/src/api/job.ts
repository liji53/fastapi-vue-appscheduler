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
  created_at: string;
};
type JobResult = {
  total: number;
  data: Array<Job>;
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
