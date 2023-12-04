import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/tasks",
    method: "get",
    response: () => {
      return {
        total: 4,
        data: [
          {
            id: 1,
            name: "获取数据",
            project: "信创",
            project_id: 1,
            app_id: 12,
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            status: true,
            updated_at: "2023-01-11 20:10:01",
            cron: "* * * * *"
          },
          {
            id: 2,
            name: "获取数据2",
            project: "信创",
            project_id: 1,
            app_id: 1,
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            status: false,
            updated_at: "2023-01-11 20:10:01",
            cron: "* * 2-10 * *"
          },
          {
            id: 3,
            name: "获取数据3",
            project: "招商",
            project_id: 2,
            app_id: 2,
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            status: true,
            updated_at: "2023-01-11 20:10:01",
            cron: "* 1,2 * * *"
          },
          {
            id: 4,
            name: "获取数据4",
            project: "信创",
            project_id: 1,
            app_id: 1,
            remark:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部",
            status: false,
            updated_at: "2023-01-11 20:10:01",
            cron: "0/3 * * * ?"
          }
        ]
      };
    }
  }
] as MockMethod[];
