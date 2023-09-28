export default {
  path: "/monitor",
  meta: {
    icon: "monitor",
    title: "监控中心",
    // showLink: false,
    rank: 8
  },
  children: [
    {
      path: "/monitor/exception",
      name: "Exception",
      component: () => import("@/views/monitor/exception.vue"),
      meta: {
        title: "异常监控"
      }
    },
    {
      path: "/monitor/statistics",
      name: "Statistics",
      component: () => import("@/views/monitor/statistics.vue"),
      meta: {
        title: "统计管理"
      }
    },
    {
      path: "/monitor/resource",
      name: "Resource",
      component: () => import("@/views/monitor/resource.vue"),
      meta: {
        title: "系统资源"
      }
    }
  ]
};
