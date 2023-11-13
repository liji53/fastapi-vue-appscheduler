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
            name: "SSL证书",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 2,
            is_online: false,
            category_id: 1,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书2",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 3,
            is_online: true,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书3",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 4,
            is_online: true,
            category_id: 2,
            banner: "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            name: "SSL证书4",
            description:
              "SSL证书又叫服务器证书，腾讯云为您提供证书的一站式服务，包括免费、付费证书的申请、管理及部"
          },
          {
            id: 5,
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
            value: "1",
            label: "规范递交",
            children: [
              {
                value: "12",
                label: "SSL证书"
              },
              {
                value: "13",
                label: "SSL证书2"
              },
              {
                value: "14",
                label: "SSL证书4"
              }
            ]
          },
          {
            value: "2",
            label: "数据比对",
            children: [
              {
                value: "15",
                label: "SSL证书4"
              },
              {
                value: "16",
                label: "SSL证书6"
              }
            ]
          }
        ]
      };
    }
  }
] as MockMethod[];
