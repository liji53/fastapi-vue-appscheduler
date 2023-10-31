import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

export type UserResult = {
  /** 用户名 */
  username: string;
  /*头像 */
  avatar: string;
  /** 当前登陆用户的角色 */
  roles: Array<string>;
  /** `token` */
  accessToken: string;
  /** 用于调用刷新`accessToken`的接口时所需的`token` */
  refreshToken: string;
  /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
  expires: Date;
};

export type RefreshTokenResult = {
  /** `token` */
  accessToken: string;
  /** 用于调用刷新`accessToken`的接口时所需的`token` */
  refreshToken: string;
  /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
  expires: Date;
};

type User = {
  id: number;
  username: string;
  avatar: string;
  phone: string;
  email: string;
  status: boolean;
  remark: string;
  created_at: string;
};

export type UserList = {
  total: number;
  data: Array<User>;
};

type RoleIds = {
  data: Array<number>;
};

/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", baseUrlApi("auth/login"), { data });
};
/** 刷新token */
export const refreshTokenApi = (data?: object) => {
  return http.request<RefreshTokenResult>(
    "post",
    baseUrlApi("auth/refresh_token"),
    {
      data
    }
  );
};

// 用户列表;
export const getUserList = (params?: object) => {
  return http.request<UserList>("get", baseUrlApi("users"), { params });
};
// 新建用户
export const createUser = (data?: object) => {
  return http.post(baseUrlApi("users"), { data });
};
// 更新用户
export const updateUser = (user_id: number, data?: object) => {
  return http.put(baseUrlApi(`users/${user_id}`), { data });
};
// 删除用户
export const deleteUser = (user_id: number) => {
  return http.delete(baseUrlApi(`users/${user_id}`));
};
// 批量删除用户
export const batchUserDelete = (data?: object) => {
  return http.delete(baseUrlApi("users"), { data });
};

/** 用户管理-根据userId，获取对应角色id列表（userId：用户id） */
export const getRoleIds = (user_id: number) => {
  return http.request<RoleIds>("get", baseUrlApi(`users/${user_id}/roles`));
};

// 上传用户头像
export const uploadUserAvatar = (user_id: number, data?: object) => {
  return http.upload(baseUrlApi(`users/${user_id}/avatar`), { data });
};
