import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/sys_resources",
    method: "get",
    response: () => {
      return {
        cpu: 0.1,
        memory: 88,
        disk: 206.4,
        full_disk: 512
      };
    }
  }
] as MockMethod[];
