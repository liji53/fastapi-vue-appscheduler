import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

type Result = {
  data: Array<any>;
};

export const getAsyncRoutes = () => {
  return http.request<Result>("get", baseUrlApi("permission/routes"));
};
