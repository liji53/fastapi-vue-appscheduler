// 模拟后端动态生成路由
import { MockMethod } from "vite-plugin-mock";

const taskRouter = {
  path: "/task",
  meta: { title: "任务中心", icon: "menu", rank: 3 },
  children: [
    {
      path: "/task/project",
      name: "Project",
      meta: {
        title: "项目管理"
      }
    },
    {
      path: "/task/job",
      name: "Job",
      meta: { title: "任务管理" }
    }
  ]
};
const appRouter = {
  path: "/app",
  meta: { title: "应用中心", icon: "menu", rank: 4 },
  children: [
    {
      path: "/app/store",
      name: "Store",
      meta: {
        title: "应用商城",
        auths: ["btn_add", "btn_update", "btn_delete"]
      }
    },
    {
      path: "/app/appForm",
      name: "AppForm",
      meta: { title: "配置设计" }
    },
    {
      path: "/app/myApp",
      name: "MyApp",
      meta: { title: "我的应用" }
    }
  ]
};
const securityRouter = {
  path: "/security",
  meta: {
    title: "安全中心",
    icon: "flUser",
    rank: 10
  },
  children: [
    {
      path: "/security/role/index",
      name: "Role",
      meta: {
        title: "角色管理"
      }
    },
    {
      path: "/security/user/index",
      name: "User",
      meta: {
        title: "用户管理"
      }
    },
    {
      path: "/security/config",
      name: "Config",
      meta: {
        title: "系统配置"
      }
    }
  ]
};
const monitorRouter = {
  path: "/monitor",
  meta: {
    title: "监控中心",
    icon: "monitor",
    rank: 8
  },
  children: [
    {
      path: "/monitor/exception",
      name: "Exception",
      meta: { title: "异常监控" }
    },
    {
      path: "/monitor/statistics",
      name: "Statistics",
      meta: { title: "统计管理" }
    },
    {
      path: "/monitor/resource",
      name: "Resource",
      meta: { title: "系统资源" }
    }
  ]
};

export default [
  {
    url: "/permission/routes",
    method: "get",
    response: () => {
      return {
        success: true,
        data: [appRouter, taskRouter, monitorRouter, securityRouter]
      };
    }
  }
] as MockMethod[];
