<script setup lang="ts">
import { ref } from "vue";
import { useApp } from "./utils/hookMyApp";
import AppCard from "./components/AppCard.vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Search from "@iconify-icons/ep/search";
import Refresh from "@iconify-icons/ep/refresh";

defineOptions({
  name: "MyApp"
});

const formRef = ref();
const appFromRef = ref();
const {
  form,
  loading,
  pagination,
  categories,
  apps,
  dialogVisable,
  dialogTitle,
  appForm,
  appFormRules,
  onSearch,
  resetForm,
  onPageSizeChange,
  onCurrentPageChange,
  onConfirmApp,
  handleUninstallApp,
  handleUploadPicApp,
  handleRevisionApp,
  handleEditApp,
  getCategoryName
} = useApp();
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px]"
    >
      <el-form-item label="应用名称：" prop="name">
        <el-input
          v-model="form.name"
          placeholder="请输入应用名称"
          clearable
          class="!w-[200px]"
        />
      </el-form-item>
      <el-form-item label="应用分类：" prop="category_id">
        <el-select
          v-model="form.category_id"
          placeholder="请选择应用分类"
          clearable
          class="!w-[180px]"
        >
          <el-option
            v-for="(item, index) in categories"
            :key="index"
            :value="item.id"
            :label="item.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态：" prop="is_online">
        <el-select
          v-model="form.is_online"
          placeholder="请选择状态"
          clearable
          class="!w-[180px]"
        >
          <el-option label="已上线" :value="true" />
          <el-option label="未上线" :value="false" />
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

    <div v-loading="loading" style="margin-top: 12px">
      <el-empty description="暂无应用" v-show="pagination.total === 0" />
      <template v-if="pagination.total > 0">
        <el-row :gutter="16">
          <el-col
            v-for="app of apps"
            :key="app.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
            :xl="4"
          >
            <AppCard
              :app="app"
              :category="getCategoryName(app.category_id)"
              pagename="myApp"
              @revision-app="handleRevisionApp"
              @edit-app="handleEditApp"
              @uninstall-app="handleUninstallApp"
              @upload-pic="handleUploadPicApp"
            />
          </el-col>
        </el-row>

        <el-pagination
          class="float-right"
          v-model:currentPage="pagination.currentPage"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[12, 24, 36]"
          background
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="onPageSizeChange"
          @current-change="onCurrentPageChange"
        />
      </template>
    </div>

    <el-dialog v-model="dialogVisable" :title="`${dialogTitle}应用`">
      <el-form
        ref="appFromRef"
        :model="appForm"
        :rules="appFormRules"
        label-width="82px"
      >
        <el-form-item label="应用名称" prop="name">
          <el-input
            v-model="appForm.name"
            clearable
            placeholder="请输入应用名称"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="appForm.description"
            placeholder="请输入描述信息"
            type="textarea"
          />
        </el-form-item>
        <el-form-item>
          <el-button @click="dialogVisable = false"> 取消 </el-button>
          <el-button type="primary" @click="onConfirmApp(appFromRef)">
            确定
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}

.custom-button {
  margin-top: 12px;
}
</style>
