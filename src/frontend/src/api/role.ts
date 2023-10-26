import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

type Role = {
  id: Number;
  name: string;
};

type RoleList = {
  total: number;
  data: Array<Role>;
};

/** 获取角色列表 */
export const getAllRoleList = (params?: object) => {
  return http.request<RoleList>("get", baseUrlApi("roles"), { params });
};
