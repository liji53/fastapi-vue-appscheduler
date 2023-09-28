export default {
  path: "/task",
  meta: {
    icon: "listCheck",
    title: "任务中心",
    // showLink: false,
    rank: 2
  },
  children: [
    {
      path: "/task/index",
      name: "Task",
      component: () => import("@/views/task/index.vue"),
      meta: {
        title: "任务中心"
      }
    }
  ]
};
