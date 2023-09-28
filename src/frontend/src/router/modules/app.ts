export default {
  path: "/app",
  meta: {
    icon: "menu",
    title: "应用中心",
    // showLink: false,
    rank: 4
  },
  children: [
    {
      path: "/app/manager",
      name: "App",
      component: () => import("@/views/app/manager.vue"),
      meta: {
        title: "应用管理"
      }
    },
    {
      path: "/app/store",
      name: "Store",
      component: () => import("@/views/app/store.vue"),
      meta: {
        title: "应用商城"
      }
    }
  ]
};
