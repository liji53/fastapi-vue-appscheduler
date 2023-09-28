<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getTaskList, addTask, updateTask, deleteTask } from "@/api/task";
import { getMyApps, getAppDefaultConfig, getAppConfigByTask } from "@/api/app";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import AddFill from "@iconify-icons/ri/add-circle-line";
import Edit from "@iconify-icons/ep/edit-pen";
import Run from "@iconify-icons/ep/video-play";
import Delete from "@iconify-icons/ep/delete";
import Clock from "@iconify-icons/ep/clock";
import Info from "@iconify-icons/ep/info-filled";
import Dialog from "./components/DialogForm.vue";
import { message } from "@/utils/message";

defineOptions({
  name: "Task"
});

const columns: TableColumnList = [
  {
    label: "任务名称",
    prop: "task_name",
    width: "200",
    fixed: true
  },
  {
    label: "状态",
    prop: "status",
    width: "200"
  },
  {
    label: "备注",
    prop: "remark",
    width: "260"
  },
  {
    label: "应用名称",
    prop: "app_name",
    width: "200"
  },
  {
    label: "创建日期",
    prop: "create_time",
    width: "250"
  },
  {
    label: "更新日期",
    prop: "update_time",
    width: "250"
  },
  {
    label: "操作",
    width: "260",
    fixed: "right",
    slot: "operation"
  }
];

const dataLoading = ref(true);
const searchValue = ref("");
const formDialogVisible = ref(false);
const formDialogTitle = ref("新建任务");
const formDialogApps = ref([]);
const formDialogData = ref({ app_name: "", task_name: "", task_remark: "" });
const formDialogAppConfig = ref({});
const formDialogCron = ref("");
const tasks = ref([]);

const getAppNames = async () => {
  try {
    const { data } = await getMyApps();
    formDialogApps.value = data.map(obj => obj.name);
  } catch (e) {
    console.log(e);
  } finally {
    setTimeout(() => {
      dataLoading.value = false;
    }, 500);
  }
};
const getTaskListData = async () => {
  try {
    const { data } = await getTaskList();
    tasks.value = data;
  } catch (e) {
    console.log(e);
  } finally {
    setTimeout(() => {
      dataLoading.value = false;
    }, 500);
  }
};

onMounted(() => {
  getAppNames();
  getTaskListData();
});

function onAdd() {
  formDialogData.value.app_name = "";
  formDialogData.value.task_name = "";
  formDialogData.value.task_remark = "";
  formDialogTitle.value = "新建任务";
  formDialogCron.value = "";
  formDialogAppConfig.value = {};
  formDialogVisible.value = true;
}

async function onEdit(row) {
  formDialogData.value.app_name = row.app_name;
  formDialogData.value.task_name = row.task_name;
  formDialogData.value.task_remark = row.remark;
  formDialogTitle.value = "编辑任务";
  formDialogCron.value = row.cron;
  try {
    const { data } = await getAppConfigByTask({ task_name: row.task_name });
    formDialogAppConfig.value = data;
  } catch (e) {
    console.log(e);
  }
  formDialogVisible.value = true;
}

function onRun(row) {
  message("运行功能暂时不支持！", { type: "error" });
}

async function onTimer(row) {
  formDialogData.value.app_name = row.app_name;
  formDialogData.value.task_name = row.task_name;
  formDialogData.value.task_remark = row.remark;
  formDialogTitle.value = "定时任务";
  formDialogCron.value = row.cron;
  try {
    const { data } = await getAppConfigByTask({ task_name: row.task_name });
    formDialogAppConfig.value = data;
  } catch (e) {
    console.log(e);
  }
  formDialogVisible.value = true;
}

async function onDelete(row) {
  try {
    await deleteTask(row.task_name);
  } catch (e) {
    console.log(e);
  }
  tasks.value = tasks.value.filter(
    obj =>
      !(
        Object.keys(obj).includes("task_name") &&
        obj["task_name"] === row.task_name
      )
  );
}

function onVersion(row) {
  message("版本功能暂时不支持！", { type: "error" });
}

const handleSelectApp = async app_name => {
  try {
    const { data } = await getAppDefaultConfig({ app_name: app_name });
    formDialogAppConfig.value = data;
  } catch (e) {
    console.log(e);
  }
};

const handleTask = async (data, app_config, cron) => {
  if (formDialogTitle.value === "新建任务") {
    try {
      await addTask({
        task: data.value,
        app_config: app_config.value,
        cron: cron.value
      });
    } catch (e) {
      console.log(e);
    }
  } else {
    try {
      await updateTask({
        task: data.value,
        app_config: app_config.value,
        cron: cron.value
      });
    } catch (e) {
      console.log(e);
    }
  }
  getTaskListData();
};

const filterTasks = computed(() =>
  tasks.value.filter(
    data =>
      !searchValue.value ||
      data.task_name.toLowerCase().includes(searchValue.value.toLowerCase())
  )
);
</script>

<template>
  <div class="main">
    <!-- 新建任务+搜索 -->
    <div class="w-full flex justify-between mb-4">
      <!-- 新建任务 -->
      <el-button :icon="useRenderIcon(AddFill)" @click="onAdd">
        新建任务
      </el-button>
      <!-- 搜索输入框 -->
      <el-input
        style="width: 300px"
        v-model="searchValue"
        placeholder="请输入任务名称"
        clearable
      >
        <template #suffix>
          <el-icon class="el-input__icon">
            <IconifyIconOffline
              v-show="searchValue.length === 0"
              :icon="Search"
            />
          </el-icon>
        </template>
      </el-input>
    </div>
    <!-- 任务列表 -->
    <pure-table :data="filterTasks" :columns="columns">
      <!-- 操作列表 -->
      <template #operation="{ row }">
        <el-tooltip
          class="box-item"
          effect="dark"
          content="编辑"
          placement="top"
        >
          <el-button
            :icon="useRenderIcon(Edit)"
            type="primary"
            @click="onEdit(row)"
            hover="编辑"
            size="small"
            circle
          />
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="dark"
          content="运行"
          placement="top"
        >
          <el-button
            :icon="useRenderIcon(Run)"
            type="primary"
            @click="onRun(row)"
            size="small"
            circle
          />
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="dark"
          content="定时"
          placement="top"
        >
          <el-button
            :icon="useRenderIcon(Clock)"
            type="primary"
            @click="onTimer(row)"
            size="small"
            circle
          />
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="dark"
          content="删除"
          placement="top"
        >
          <el-button
            :icon="useRenderIcon(Delete)"
            type="danger"
            @click="onDelete(row)"
            size="small"
            circle
          />
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="dark"
          content="版本信息"
          placement="top"
        >
          <el-button
            :icon="useRenderIcon(Info)"
            type="info"
            @click="onVersion(row)"
            size="small"
            circle
          />
        </el-tooltip>
      </template>
    </pure-table>
    <Dialog
      v-model:visible="formDialogVisible"
      :title="formDialogTitle"
      :app_names="formDialogApps"
      :data="formDialogData"
      :app_config="formDialogAppConfig"
      :cron="formDialogCron"
      @select-app="handleSelectApp"
      @commit-task="handleTask"
    />
  </div>
</template>
