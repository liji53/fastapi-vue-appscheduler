<script setup lang="ts">
import { useException } from "./utils/hookException";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref } from "vue";

import Delete from "@iconify-icons/ep/delete";
import Search from "@iconify-icons/ep/search";
import Refresh from "@iconify-icons/ep/refresh";
import Document from "@iconify-icons/ep/document";

const formRef = ref();
defineOptions({
  name: "Exception"
});

const {
  form,
  loading,
  columns,
  logList,
  taskTree,
  taskTreeProps,
  pagination,
  onSearch,
  resetForm,
  openDialog,
  handleDelete,
  handleSizeChange,
  handleCurrentChange,
  dialogVisible,
  logTxt
} = useException();
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px]"
    >
      <el-form-item label="任务名称：" prop="task_ids">
        <el-tree-select
          v-model="form.task_ids"
          :props="taskTreeProps"
          :data="taskTree"
          :render-after-expand="false"
          placeholder="请选择任务"
          clearable
          multiple
          collapse-tags
          class="!w-[280px]"
        />
      </el-form-item>
      <el-form-item label="执行状态：" prop="status">
        <el-select
          v-model="form.status"
          placeholder="请选择执行状态"
          clearable
          class="!w-[180px]"
        >
          <el-option label="成功" value="true" />
          <el-option label="失败" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="日志等级：" prop="log_type">
        <el-select
          v-model="form.log_type"
          placeholder="请选择日志等级"
          clearable
          class="!w-[180px]"
        >
          <el-option label="致命" value="fatal" />
          <el-option label="错误" value="error" />
          <el-option label="警告" value="warning" />
          <el-option label="其他" value="other" />
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

    <PureTableBar title="日志列表" :columns="columns" @refresh="onSearch">
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          align-whole="center"
          showOverflowTooltip
          table-layout="auto"
          :loading="loading"
          :size="size"
          adaptive
          :data="logList"
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
            <el-button
              link
              type="primary"
              :size="size"
              :icon="useRenderIcon(Document)"
              @click="openDialog(row)"
            >
              日志
            </el-button>
            <el-popconfirm
              title="是否确认删除日志"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button
                  class="reset-margin"
                  link
                  type="primary"
                  :size="size"
                  :icon="useRenderIcon(Delete)"
                >
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </pure-table>
      </template>
    </PureTableBar>

    <el-dialog v-model="dialogVisible" title="日志详情" fullscreen>
      <el-input
        v-if="logTxt != ''"
        type="textarea"
        disabled
        v-model="logTxt"
        autosize
        input-style="background-color: black;color: white;"
      />
      <div v-else>本次执行没有日志打印</div>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
