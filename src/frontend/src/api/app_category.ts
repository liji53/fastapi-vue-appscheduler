import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

export type AppCategory = {
  id: number;
  name: string;
  description: string;
};
type AppCategoryResult = {
  data: Array<AppCategory>;
};

// app分类
export const getAppCategory = () => {
  return http.request<AppCategoryResult>("get", baseUrlApi("app_categories"));
};
