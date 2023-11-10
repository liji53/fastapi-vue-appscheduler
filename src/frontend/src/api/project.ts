import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type Project = {
  id: number;
  name: string;
  remark: string;
  task_count: number;
  running_count: number;
  failed_count: number;
  created_at: string;
};
type ProjectResult = {
  total: number;
  data: Array<Project>;
};

export const getProjectList = (params?: object) => {
  return http.request<ProjectResult>("get", baseUrlApi("projects"), { params });
};

export const createProject = (data: object) => {
  return http.post(baseUrlApi("projects"), { data });
};

export const updateProject = (project_id: number, data: object) => {
  return http.put(baseUrlApi(`projects/${project_id}`), { data });
};

export const deleteProject = (project_id: number) => {
  return http.delete(baseUrlApi(`projects/${project_id}`));
};
