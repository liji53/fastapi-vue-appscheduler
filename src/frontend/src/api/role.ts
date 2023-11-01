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

type Menu = {
  id: Number;
  title: string;
  children: Array<Menu>;
};

type MenuList = {
  // 所有的菜单
  menus: Array<Menu>;
  // 当前角色已经拥有的菜单
  activedMenus: Array<number>;
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

// 获取指定角色的Menus
export const getRoleMenus = (role_id: number) => {
  return http.request<MenuList>("get", baseUrlApi(`roles/${role_id}/menus`));
};
