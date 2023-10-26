// 根据角色动态生成路由
import { MockMethod } from "vite-plugin-mock";

export default [
  // 用户管理-获取所有用户列表
  {
    url: "/users",
    method: "get",
    response: () => {
      const list = [
        {
          username: "admin",
          avatar: null,
          phone: null,
          email: null,
          id: 1,
          status: true,
          remark: null,
          created_at: "2023-10-25T08:18:28Z"
        },
        {
          username: "common",
          avatar: "https://avatars.githubusercontent.com/u/52823142",
          phone: "18288882345",
          email: "@email",
          id: 2,
          status: true,
          remark: "普通用户",
          created_at: 1605456000000
        }
      ];
      return {
        total: list.length,
        data: list
      };
    }
  },
  // 用户管理-根据userId，获取对应角色id列表（userId：用户id）
  {
    url: "/users/1/roles",
    method: "get",
    response: () => {
      return [1];
    }
  }
] as MockMethod[];
