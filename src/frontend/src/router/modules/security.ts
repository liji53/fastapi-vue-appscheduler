export default {
  path: "/security",
  meta: {
    icon: "flUser",
    title: "安全中心",
    rank: 10
  },
  children: [
    {
      path: "/security/user",
      name: "User",
      component: () => import("@/views/security/user.vue"),
      meta: {
        title: "用户管理"
      }
    },
    // {
    //   path: "/security/role",
    //   name: "Role",
    //   component: () => import("@/views/security/role.vue"),
    //   meta: {
    //     title: "角色管理"
    //   }
    // },
    // {
    //   path: "/security/menu",
    //   name: "Page",
    //   component: () => import("@/views/security/Menu.vue"),
    //   meta: {
    //     title: "页面权限"
    //   }
    // },
    {
      path: "/security/config",
      name: "Config",
      component: () => import("@/views/security/config.vue"),
      meta: {
        title: "系统配置"
      }
    }
  ]
};
