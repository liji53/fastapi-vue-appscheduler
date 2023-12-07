import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";

export type AppCategory = {
  id: number;
  name: string;
  description: string;
};
type AppCategoryResult = {
  total: number;
  data: Array<AppCategory>;
};

// app分类
export const getAppCategory = (params?: object) => {
  return http.request<AppCategoryResult>("get", baseUrlApi("app_categories"), {
    params
  });
};

export const createCategory = (data: object) => {
  return http.post(baseUrlApi("app_categories"), { data });
};

export const updateCategory = (category_id: number, data: object) => {
  return http.put(baseUrlApi(`app_categories/${category_id}`), { data });
};

export const deleteCategory = (category_id: number) => {
  return http.delete(baseUrlApi(`app_categories/${category_id}`));
};
