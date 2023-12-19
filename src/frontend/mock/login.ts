// 根据角色动态生成路由
import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/auth/login",
    method: "post",
    response: ({ body }) => {
      if (body.username === "admin") {
        return {
          username: "admin",

          // 一个用户可能有多个角色
          roles: ["admin"],
          accessToken: "eyJhbGciOiJIUzUxMiJ9.admin",
          refreshToken: "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
          expires: "2023/12/31 00:00:00",
          avatar: null
        };
      } else {
        return {
          username: "common",
          // 一个用户可能有多个角色
          roles: ["common"],
          accessToken: "eyJhbGciOiJIUzUxMiJ9.common",
          refreshToken: "eyJhbGciOiJIUzUxMiJ9.commonRefresh",
          expires: "2023/12/30 00:00:00",
          avatar: null
        };
      }
    }
  },
  {
    url: "/auth/refresh_token",
    method: "post",
    response: ({ body }) => {
      if (body.username === "admin") {
        return {
          accessToken: "eyJhbGciOiJIUzUxMiJ9.admin",
          refreshToken: "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
          expires: "2024/10/30 00:00:00"
        };
      } else {
        return {
          username: "common",
          // 一个用户可能有多个角色
          roles: ["common"],
          accessToken: "eyJhbGciOiJIUzUxMiJ9.common",
          refreshToken: "eyJhbGciOiJIUzUxMiJ9.commonRefresh",
          expires: "2024/10/30 00:00:00",
          avatar: null
        };
      }
    }
  }
] as MockMethod[];
