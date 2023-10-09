// 参考：https://yiming_chang.gitee.io/pure-admin-doc/pages/request/
export const baseUrlApi = (url: string) =>
  process.env.NODE_ENV === "development" ? `/${url}` : `/api/v1/${url}`;
