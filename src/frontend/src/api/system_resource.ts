import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

export type resourceResult = {
  cpu: number;
  memory: number;
  disk: number;
  full_disk: number;
};

// 系统资源：cpu、内存、硬盘
export const getSystemResource = () => {
  return http.request<resourceResult>("get", baseUrlApi("sys_resources"));
};
