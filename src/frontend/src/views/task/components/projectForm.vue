<script setup lang="ts">
import { ref } from "vue";
import { projectFormRules } from "../utils/rule";
import { ProjectFormProps } from "../utils/types";

const props = withDefaults(defineProps<ProjectFormProps>(), {
  formInline: () => ({
    name: "",
    remark: ""
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
    :rules="projectFormRules"
    label-width="82px"
  >
    <el-form-item label="项目名称" prop="name">
      <el-input
        v-model="newFormInline.name"
        clearable
        placeholder="请输入项目名称"
      />
    </el-form-item>

    <el-form-item label="备注">
      <el-input
        v-model="newFormInline.remark"
        placeholder="请输入备注信息"
        type="textarea"
      />
    </el-form-item>
  </el-form>
</template>
