import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/task_logs",
    method: "get",
    response: () => {
      return {
        total: 4,
        data: [
          {
            id: 1,
            project_name: "测试项目",
            task_name: "测试任务1",
            status: true,
            log_type: "error",
            execute_type: "手动",
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 2,
            project_name: "开发项目",
            task_name: "开发任务1",
            status: false,
            log_type: "fatal",
            execute_type: "手动",
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 3,
            project_name: "测试项目",
            task_name: "测试任务1",
            status: true,
            log_type: "other",
            execute_type: "定时",
            created_at: "2023-01-11 20:10:01"
          },
          {
            id: 4,
            project_name: "测试项目",
            task_name: "测试任务3",
            status: true,
            log_type: "warning",
            execute_type: "手动",
            created_at: "2023-01-11 20:10:01"
          }
        ]
      };
    }
  },
  {
    url: "/logs/1/content",
    method: "get",
    response: () => {
      return {
        data: "?????\n日志 打印"
      };
    }
  },
  {
    url: "/task_logs/recently",
    method: "get",
    response: () => {
      return {
        id: 1,
        project_name: "测试项目",
        task_name: "测试任务1",
        status: true,
        log_type: "error",
        execute_type: "手动",
        created_at: "2023-01-11 20:10:01",
        content: "?????\n运行日志\n打印"
      };
    }
  }
] as MockMethod[];
