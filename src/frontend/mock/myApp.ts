import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/installed_apps",
    method: "get",
    response: () => {
      return {
        total: 8,
        data: [
          {
            id: 1,
            is_online: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Documents/D5.Others/产品质量提升工具脚本/S6_项目辅助类工具/[16]批量提取doc文档目录",
            name: "SSL证书",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 2,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Sources/DevCodes/SqlPatch",
            is_online: false,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书2",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 3,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Sources/DevCodes/SqlPatch",
            is_online: true,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书3",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 4,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Sources/DevCodes/SqlPatch",
            is_online: true,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书4",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 5,
            url: "https://192.168.57.30/secu/dep1/UftdbSett/trunk/Sources/DevCodes/SqlPatch",
            is_online: false,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书5",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 6,
            is_online: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书6",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 7,
            is_online: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书7",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 8,
            is_online: true,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书8",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          }
        ]
      };
    }
  },
  {
    url: "/installed_apps/tree",
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
  }
] as MockMethod[];
