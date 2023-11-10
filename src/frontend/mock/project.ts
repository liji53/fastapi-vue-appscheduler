import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/projects",
    method: "get",
    response: () => {
      return {
        total: 4,
        data: [
          {
            id: 1,
            name: "信创",
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            task_count: 2,
            running_count: 0,
            failed_count: 0,
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 2,
            name: "招商",
            remark: null,
            task_count: 20,
            running_count: 0,
            failed_count: 1,
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 3,
            name: "国泰",
            remark: "SSL",
            task_count: 0,
            running_count: 0,
            failed_count: 0,
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 4,
            name: "中信",
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            task_count: 2,
            running_count: 0,
            failed_count: 0,
            created_at: "2023-01-11 20:10:01"
          }
        ]
      };
    }
  }
] as MockMethod[];
