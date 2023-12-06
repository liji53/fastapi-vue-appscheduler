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
  },
  {
    url: "/tasks/1/config",
    method: "get",
    response: () => {
      return {
        data: JSON.stringify([
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "mGdLbChWNP2iPCZxvhsns",
            layout: false,
            data: {
              fieldName: "doc文档目录",
              label: "doc文档目录",
              tip: "",
              placeholder: "请输入文档路径",
              showRule: "{}",
              required: true,
              rule: "[]",
              default: "",
              csslist: []
            }
          },
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "tZ8bW7QEHP5Y5tgRh1O89",
            layout: false,
            data: {
              fieldName: "生成execl的目录",
              label: "生成execl的目录",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: "./dist"
            }
          },
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "X-ovka9WGnkNoqMj50uQE",
            layout: false,
            data: {
              fieldName: "指定doc文件名包含内容",
              label: "指定doc文件名包含内容",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: ""
            }
          }
        ])
      };
    }
  },
  {
    url: "/tasks/2/config",
    method: "get",
    response: () => {
      return {
        data: JSON.stringify([
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "mGdLbChWNP2iPCZxvhsns",
            layout: false,
            data: {
              fieldName: "doc文档目录",
              label: "doc文档目录",
              tip: "",
              placeholder: "请输入文档路径",
              showRule: "{}",
              required: true,
              rule: "[]",
              default: "./src",
              csslist: []
            }
          },
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "tZ8bW7QEHP5Y5tgRh1O89",
            layout: false,
            data: {
              fieldName: "生成execl的目录",
              label: "生成execl的目录",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: "./dist"
            }
          },
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "X-ovka9WGnkNoqMj50uQE",
            layout: false,
            data: {
              fieldName: "指定doc文件名包含内容",
              label: "指定doc文件名包含内容",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: ""
            }
          }
        ])
      };
    }
  },
  {
    url: "/tasks/tree",
    method: "get",
    response: () => {
      return {
        data: [
          {
            name: "测试项目",
            children: [
              {
                id: 1,
                name: "测试任务1"
              },
              {
                id: 2,
                name: "测试任务2"
              },
              {
                id: 3,
                name: "测试任务3"
              }
            ]
          },
          {
            name: "开发项目",
            children: [
              {
                id: 7,
                name: "开发任务1"
              },
              {
                id: 8,
                name: "开发任务2"
              }
            ]
          }
        ]
      };
    }
  }
] as MockMethod[];
