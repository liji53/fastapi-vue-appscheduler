import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/apps",
    method: "get",
    response: () => {
      return {
        total: 4,
        data: [
          {
            id: 1,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: true,
            is_installed: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 2,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: false,
            is_installed: false,
            category_id: null,
            banner: "https://tdesign.gtimg.com/tdesign-pro/t-sec.jpg",
            name: "人脸识别",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 3,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: false,
            is_installed: false,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
            name: "CVM",
            description:
              "云硬盘为您提供用于CVM的持久性数据块级存储服务。云硬盘中的数据自动地可用区内以多副本冗"
          },
          {
            id: 4,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: true,
            is_installed: false,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
            name: "SSL证书",
            description:
              "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
          },
          {
            id: 5,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: true,
            is_installed: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
            name: "SSL证书",
            description:
              "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
          },
          {
            id: 6,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: true,
            is_installed: true,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
            name: "SSL证书",
            description:
              "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
          },
          {
            id: 7,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S5_任务跟踪类/Track/IntegratedNoMergedTrack",
            status: false,
            is_installed: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
            name: "SSL证书",
            description:
              "云数据库MySQL为用户提供安全可靠，性能卓越、易于维护的企业级云数据库服务。"
          }
        ]
      };
    }
  },
  {
    url: "/app_categories",
    method: "get",
    response: () => {
      return {
        data: [
          {
            id: 1,
            name: "规范递交",
            app_count: 2,
            installed_app_count: 2,
            installed_sum_count: 4,
            created_at: "2023-01-11 20:10:01",
            description: "检查程序规范化递交"
          },
          {
            id: 2,
            name: "数据比对",
            app_count: 3,
            installed_app_count: 2,
            installed_sum_count: 9,
            created_at: "2023-01-11 20:10:01",
            description: "数据库的数据比对工具"
          }
        ]
      };
    }
  },
  {
    url: "/apps/tree",
    method: "get",
    response: () => {
      return {
        data: [
          {
            id: 1,
            name: "规范递交",
            children: [
              {
                id: 12,
                name: "SSL证书"
              },
              {
                id: 13,
                name: "SSL证书2"
              },
              {
                id: 14,
                name: "SSL证书4"
              }
            ]
          },
          {
            id: 2,
            name: "数据比对",
            children: [
              {
                id: 15,
                name: "SSL证书4"
              },
              {
                id: 16,
                name: "SSL证书6"
              }
            ]
          }
        ]
      };
    }
  },
  {
    url: "/apps/1/readme",
    method: "get",
    response: () => {
      return {
        data: "# 批量提取doc文档的目录\n\
### 功能描述\n\
用于提取指定目录下的doc文档的目录，并将目录结构保存成execl文档。\n\
一个doc文档会对应的生成一个execl文档。\n\
### 配置说明\n\
略\n"
      };
    }
  }
] as MockMethod[];
