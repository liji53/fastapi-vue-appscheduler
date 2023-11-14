import { reactive } from "vue";
import type { FormRules } from "element-plus";

/** 自定义表单规则校验 */
export const projectFormRules = reactive(<FormRules>{
  name: [{ required: true, message: "项目名称为必填项", trigger: "blur" }]
});

export const jobFormRules = reactive(<FormRules>{
  app_id: [{ required: true, message: "必须选择一个应用", trigger: "blur" }],
  name: [{ required: true, message: "必须填写任务名称", trigger: "blur" }],
  project_id: [{ required: true, message: "必须选择一个项目", trigger: "blur" }]
});
