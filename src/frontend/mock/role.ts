// 根据角色动态生成路由
import { MockMethod } from "vite-plugin-mock";

export default [
  // 用户管理-获取所有角色列表
  {
    url: "/roles",
    method: "get",
    response: () => {
      return {
        total: 6,
        data: [
          {
            name: "管理员",
            code: "admin",
            status: true,
            remark: null,
            id: 1,
            created_at: "2023-10-27T05:54:58Z"
          },
          {
            name: "普通人员",
            code: "common",
            status: true,
            remark: "普通",
            id: 2,
            created_at: "2023-10-27T06:04:15Z"
          },
          {
            name: "test",
            code: "test",
            status: true,
            remark: "",
            id: 3,
            created_at: "2023-10-27T06:04:29Z"
          },
          {
            name: "牛逼",
            code: "nibi",
            status: false,
            remark: "te",
            id: 6,
            created_at: "2023-10-27T06:06:05Z"
          },
          {
            name: "b",
            code: "b",
            status: true,
            remark: "",
            id: 8,
            created_at: "2023-10-27T06:06:15Z"
          },
          {
            name: "清算组",
            code: "bus",
            status: true,
            remark: "1",
            id: 9,
            created_at: "2023-10-27T08:07:36Z"
          }
        ]
      };
    }
  },
  // 用户管理-获取角色菜单
  {
    url: "/roles/1/menus",
    method: "get",
    response: () => {
      return {
        menus: [
          {
            id: 6,
            title: "监控中心",
            children: [
              {
                id: 7,
                title: "异常监控",
                children: null
              },
              {
                id: 8,
                title: "统计管理",
                children: null
              },
              {
                id: 9,
                title: "系统资源",
                children: null
              }
            ]
          },
          {
            id: 10,
            title: "安全中心",
            children: [
              {
                id: 12,
                title: "角色管理",
                children: null
              },
              {
                id: 11,
                title: "用户管理",
                children: null
              },
              {
                id: 13,
                title: "系统配置",
                children: null
              }
            ]
          },
          {
            id: 1,
            title: "任务中心",
            children: [
              {
                id: 2,
                title: "任务中心",
                children: null
              }
            ]
          },
          {
            id: 3,
            title: "应用中心",
            children: [
              {
                id: 4,
                title: "应用管理",
                children: null
              },
              {
                id: 5,
                title: "应用商城",
                children: null
              }
            ]
          }
        ],
        activedMenus: []
      };
    }
  },
  {
    url: "/roles/2/menus",
    method: "get",
    response: () => {
      return {
        menus: [
          {
            id: 6,
            title: "监控中心",
            children: [
              {
                id: 7,
                title: "异常监控",
                children: null
              },
              {
                id: 8,
                title: "统计管理",
                children: null
              },
              {
                id: 9,
                title: "系统资源",
                children: null
              }
            ]
          },
          {
            id: 10,
            title: "安全中心",
            children: [
              {
                id: 12,
                title: "角色管理",
                children: null
              },
              {
                id: 11,
                title: "用户管理",
                children: null
              },
              {
                id: 13,
                title: "系统配置",
                children: null
              }
            ]
          },
          {
            id: 1,
            title: "任务中心",
            children: [
              {
                id: 2,
                title: "任务中心",
                children: null
              }
            ]
          },
          {
            id: 3,
            title: "应用中心",
            children: [
              {
                id: 4,
                title: "应用管理",
                children: null
              },
              {
                id: 5,
                title: "应用商城",
                children: null
              }
            ]
          }
        ],
        activedMenus: [7, 12, 2, 4, 8, 11, 9, 13, 5]
      };
    }
  }
] as MockMethod[];
