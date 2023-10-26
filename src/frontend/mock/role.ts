// 根据角色动态生成路由
import { MockMethod } from "vite-plugin-mock";

export default [
  // 用户管理-获取所有角色列表
  {
    url: "/roles",
    method: "get",
    response: () => {
      return {
        total: 2,
        data: [
          { id: 1, name: "超级管理员" },
          { id: 2, name: "普通角色" }
        ]
      };
    }
  }
] as MockMethod[];
