<script setup lang="ts">
import { useJob } from "./utils/hookJob";
import crontab from "./components/crontab.vue";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref } from "vue";

import Search from "@iconify-icons/ep/search";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";
import Run from "@iconify-icons/ep/video-play";
import Clock from "@iconify-icons/ep/clock";
import Setting from "@iconify-icons/ep/setting";
import Delete from "@iconify-icons/ep/delete";
import EditPen from "@iconify-icons/ep/edit-pen";
import ArrowDown from "@iconify-icons/ep/arrow-down";

defineOptions({
  name: "Job"
});

const formRef = ref();
const {
  form,
  loading,
  columns,
  dataList,
  projects,
  pagination,
  onSearch,
  resetForm,
  openDialog,
  handleDelete,
  handleRun,
  handleTimer,
  handleConfig,
  handleSizeChange,
  handleCurrentChange,
  crontabVisible,
  isShowCronCore,
  cronFormData,
  //onChangeCron,
  onCancelCron,
  onConfirmCron
} = useJob();
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px]"
    >
      <el-form-item label="任务名称：" prop="name">
        <el-input
          v-model="form.name"
          placeholder="请输入任务名称"
          clearable
          class="!w-[200px]"
        />
      </el-form-item>
      <el-form-item label="项目：" prop="project_id">
        <el-select
          v-model="form.project_id"
          placeholder="请选择项目"
          clearable
          class="!w-[180px]"
        >
          <el-option
            v-for="(item, index) in projects"
            :key="index"
            :value="item.id"
            :label="item.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          placeholder="请选择状态"
          clearable
          class="!w-[180px]"
        >
          <el-option label="启用" value="true" />
          <el-option label="停用" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :icon="useRenderIcon(Search)"
          :loading="loading"
          @click="onSearch"
        >
          搜索
        </el-button>
        <el-button :icon="useRenderIcon(Refresh)" @click="resetForm(formRef)">
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <PureTableBar title="任务列表" :columns="columns" @refresh="onSearch">
      <template #buttons>
        <el-button
          type="primary"
          :icon="useRenderIcon(AddFill)"
          @click="openDialog()"
        >
          新增任务
        </el-button>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          align-whole="center"
          showOverflowTooltip
          table-layout="auto"
          :loading="loading"
          :size="size"
          adaptive
          :data="dataList"
          :columns="dynamicColumns"
          :pagination="pagination"
          :paginationSmall="size === 'small' ? true : false"
          :header-cell-style="{
            background: 'var(--el-fill-color-light)',
            color: 'var(--el-text-color-primary)'
          }"
          @page-size-change="handleSizeChange"
          @page-current-change="handleCurrentChange"
        >
          <template #operation="{ row }">
            <el-tooltip
              class="box-item"
              effect="dark"
              content="编辑"
              placement="top"
            >
              <el-button
                type="primary"
                size="small"
                :icon="useRenderIcon(EditPen)"
                @click="openDialog('编辑', row)"
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
                type="info"
                size="small"
                :icon="useRenderIcon(Run)"
                @click="handleRun(row)"
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
                type="success"
                size="small"
                :icon="useRenderIcon(Clock)"
                @click="handleTimer(row)"
                circle
              />
            </el-tooltip>
            <el-tooltip
              class="box-item"
              effect="dark"
              content="配置"
              placement="top"
            >
              <el-button
                type="warning"
                size="small"
                :icon="useRenderIcon(Setting)"
                @click="handleConfig(row)"
                circle
              />
            </el-tooltip>
            <el-popconfirm
              :title="`是否确认删除项目 ${row.name}`"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  size="small"
                  :icon="useRenderIcon(Delete)"
                  circle
                />
              </template>
            </el-popconfirm>
          </template>
        </pure-table>
      </template>
    </PureTableBar>

    <el-drawer
      v-model="crontabVisible"
      direction="rtl"
      :destroy-on-close="true"
      title="任务定时"
      size="800px"
    >
      <div class="pr-20">
        <el-form
          class="edit-form"
          :model="cronFormData"
          ref="formRef"
          label-width="100px"
        >
          <el-form-item label="cron表达式" prop="cron">
            <el-input
              v-model="cronFormData.cron"
              placeholder="请输入cron表达式"
            >
              <template #append>
                <el-tooltip content="配置cron表达式" placement="top">
                  <el-button
                    :icon="useRenderIcon(ArrowDown)"
                    @click="
                      () => {
                        isShowCronCore = !isShowCronCore;
                      }
                    "
                  />
                </el-tooltip>
              </template>
            </el-input>
          </el-form-item>
          <div
            style="width: 100%; padding-left: 10px; margin-top: -5px"
            v-show="isShowCronCore"
          >
            <crontab v-model:value="cronFormData.cron" />
          </div>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancelCron">取 消</el-button>
          <el-button type="primary" @click="onConfirmCron">确 定</el-button>
        </span>
      </template>
    </el-drawer>
  </div>
</template>

<style scoped lang="scss">
:deep(.el-dropdown-menu__item i) {
  margin: 0;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
