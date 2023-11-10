<script setup lang="ts">
import { ref } from "vue";
import { jobFormRules } from "../utils/rule";
import { JobFormProps } from "../utils/types";

const props = withDefaults(defineProps<JobFormProps>(), {
  formInline: () => ({
    name: "",
    remark: "",
    project_id: null,
    app_id: null,
    projects: [],
    apps: []
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
    :rules="jobFormRules"
    label-width="82px"
  >
    <el-form-item label="应用" prop="app_id">
      <el-select
        v-model="newFormInline.app_id"
        placeholder="请选择应用"
        clearable
      >
        <el-option
          v-for="(item, index) in newFormInline.apps"
          :key="index"
          :value="item.id"
          :label="item.name"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="任务名称" prop="name">
      <el-input
        v-model="newFormInline.name"
        clearable
        placeholder="请输入任务名称"
      />
    </el-form-item>

    <el-form-item label="项目" prop="project_id">
      <el-select
        v-model="newFormInline.project_id"
        placeholder="请选择项目"
        clearable
      >
        <el-option
          v-for="(item, index) in newFormInline.projects"
          :key="index"
          :value="item.id"
          :label="item.name"
        />
      </el-select>
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
