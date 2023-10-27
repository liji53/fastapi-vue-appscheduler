import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type Role = {
  id: Number;
  name: string;
  code: string;
  status: boolean;
  remark: string;
  created_at: string;
};

type RoleList = {
  total: number;
  data: Array<Role>;
};

/** 获取角色列表 */
export const getRoleList = (params?: object) => {
  return http.request<RoleList>("get", baseUrlApi("roles"), { params });
};
// 新建角色
export const createRole = (data: object) => {
  return http.post(baseUrlApi("roles"), { data });
};
// 更新角色
export const updateRole = (role_id: number, data: object) => {
  return http.put(baseUrlApi(`roles/${role_id}`), { data });
};
// 删除角色
export const deleteRole = (role_id: number) => {
  return http.delete(baseUrlApi(`roles/${role_id}`));
};
