<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { message } from "@/utils/message";

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ""
  },
  app_names: {
    type: Array<string>,
    default: () => {
      return [];
    }
  },
  data: {
    type: Object,
    default: () => {
      return {};
    }
  },
  app_config: {
    type: Object,
    default: () => {
      return {};
    }
  },
  cron: {
    type: String,
    default: ""
  }
});

const emit = defineEmits(["update:visible", "select-app", "commit-task"]);

const dialogVisible = ref(false);
const dialogTitle = ref(props.title);
const apps = ref(props.app_names); // 已安装的app列表
const dialogData = ref(props.data);
const dialogIndex = ref(0);
const appConfig = ref(props.app_config);
const cron = ref(props.cron);

const onSelectApp = async (app_name: string) => {
  emit("select-app", app_name);
};

const handleCancel = () => {
  dialogVisible.value = false;
  dialogIndex.value = 0;
};
const handlePrevPage = () => {
  dialogIndex.value--;
};
const handleNextPage = () => {
  if (
    (dialogData.value.app_name === "" || dialogData.value.task_name === "") &&
    dialogIndex.value === 0
  ) {
    message("请先选择应用程序,并输入任务名称", { type: "error" });
    return;
  }
  dialogIndex.value++;
};

const handleSubmit = () => {
  emit("commit-task", dialogData, appConfig, cron);
  dialogVisible.value = false;
  dialogIndex.value = 0;
};

watch(
  () => dialogVisible.value,
  val => {
    emit("update:visible", val);
  }
);

watch(
  () => props.visible,
  val => {
    dialogVisible.value = val;
  }
);

watch(
  () => props.title,
  val => {
    dialogTitle.value = val;
  }
);

watch(
  () => props.app_names,
  val => {
    apps.value = val;
  }
);

watch(
  () => props.data,
  val => {
    dialogData.value = val;
  }
);

watch(
  () => props.app_config,
  val => {
    appConfig.value = val;
  }
);

watch(
  () => props.cron,
  val => {
    cron.value = val;
  }
);

const dialogPage = computed(() => {
  return dialogTitle.value === "定时任务" ? 2 : dialogIndex.value;
});
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    :width="680"
    draggable
    :before-close="handleCancel"
  >
    <!-- 表单内容 -->
    <el-form :model="dialogData" label-width="100px">
      <template v-if="dialogPage === 0">
        <el-form-item label="应用程序" :required="true">
          <el-select
            v-model="dialogData.app_name"
            clearable
            :style="{ width: '480px' }"
            @change="onSelectApp"
            :disabled="dialogTitle != '新建任务'"
          >
            <el-option
              v-for="item in apps"
              :key="item"
              :value="item"
              :label="item"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="任务名称" :required="true">
          <el-input
            v-model="dialogData.task_name"
            :style="{ width: '480px' }"
            placeholder="请输入任务名称"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="dialogData.task_remark"
            type="textarea"
            :style="{ width: '480px' }"
            placeholder="请输入内容"
          />
        </el-form-item>
      </template>
      <template v-else-if="dialogPage === 1">
        <template v-for="(value, key) in appConfig" :key="key">
          <el-form-item :label="value['label']" :required="value['required']">
            <el-date-picker
              v-if="value['uiType'] === 'date-picker'"
              v-model="value['value']"
            />
            <component
              v-else
              :is="'el-' + value['uiType']"
              v-model="value['value']"
              :multiple="value['multiple']"
            >
              <template v-if="value['uiType'] === 'select'">
                <el-option
                  v-for="option in value['options']"
                  :label="option"
                  :key="option"
                  :value="option"
                />
              </template>
            </component>
          </el-form-item>
        </template>
      </template>
      <template v-else>
        <el-form-item label="cron表达式">
          <el-input
            v-model="cron"
            :style="{ width: '480px' }"
            placeholder="请输入cron表达式"
          />
        </el-form-item>
      </template>
    </el-form>
    <template #footer>
      <el-button v-if="dialogPage !== 0" @click="handlePrevPage">
        上一页
      </el-button>
      <el-button @click="handleCancel">取消</el-button>
      <el-button v-if="dialogPage !== 2" @click="handleNextPage">
        下一页
      </el-button>
      <el-button v-if="dialogPage === 2" type="primary" @click="handleSubmit">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>
