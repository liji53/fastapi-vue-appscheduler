import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/tasks/list",
    method: "get",
    response: () => {
      return {
        success: true,
        data: [
          {
            task_name: "任务1",
            status: "执行中",
            remark: "用于test",
            app_name: "ob与oracle数据比对",
            cron: "* * * * *",
            create_time: "2022-12-11 09:09:11",
            update_time: "2022-12-11 09:09:11"
          },
          {
            task_name: "任务2",
            status: "定时中",
            remark: "用于test2",
            app_name: "ob与oracle数据比对",
            cron: "* * * * 7",
            create_time: "2022-12-11 09:09:11",
            update_time: "2022-12-11 09:09:11"
          },
          {
            task_name: "任务3",
            status: "未上线",
            remark: "用于test3",
            app_name: "ob与oracle数据比对",
            cron: "1/2 * * * *",
            create_time: "2022-12-11 09:09:11",
            update_time: "2022-12-11 09:09:11"
          }
        ]
      };
    }
  },
  {
    url: "/tasks",
    method: "post",
    response: () => {
      return {
        success: true
      };
    }
  },
  {
    url: "/tasks",
    method: "put",
    response: () => {
      return {
        success: true
      };
    }
  },
  {
    url: "/tasks",
    method: "delete",
    response: () => {
      return {
        success: true
      };
    }
  }
] as MockMethod[];
