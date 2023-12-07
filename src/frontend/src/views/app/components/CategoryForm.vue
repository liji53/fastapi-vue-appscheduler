<script setup lang="ts">
import { ref, reactive } from "vue";

interface CategoryItemProps {
  // 主键
  id?: number;
  /** 名称 */
  name: string;
  /** 备注 */
  description: string;
}

interface AppCategoryFormProps {
  formInline: CategoryItemProps;
}

const FormRules = reactive({
  name: [{ required: true, message: "项目名称为必填项", trigger: "blur" }]
});

const props = withDefaults(defineProps<AppCategoryFormProps>(), {
  formInline: () => ({
    name: "",
    description: ""
  })
});

const ruleFormRef = ref();
const newFormInline = ref(props.formInline);

function getRef() {
  return ruleFormRef.value;
}

defineExpose({ getRef });
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="newFormInline"
    :rules="FormRules"
    label-width="82px"
  >
    <el-form-item label="应用分类" prop="name">
      <el-input
        v-model="newFormInline.name"
        clearable
        placeholder="请输入应用分类名称"
      />
    </el-form-item>

    <el-form-item label="描述">
      <el-input
        v-model="newFormInline.description"
        placeholder="请输入描述信息"
        type="textarea"
      />
    </el-form-item>
  </el-form>
</template>
