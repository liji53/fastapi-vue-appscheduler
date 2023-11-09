<script setup lang="ts">
import { ref } from "vue";
import { useApp } from "./utils/hookStore";
import AppCard from "./components/AppCard.vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { hasAuth } from "@/router/utils";
import Search from "@iconify-icons/ep/search";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";

defineOptions({
  name: "Store"
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
  onAddApp,
  onConfirmApp,
  handleInstallApp,
  handleRevisionApp,
  handleEditApp,
  handleDisableApp,
  handleEnableApp,
  handleDeleteApp,
  handleUploadPicApp,
  getCategoryName
} = useApp();
</script>

<template>
  <div class="main">
    <el-row :gutter="12">
      <el-col :span="hasAuth('btn_add') ? 22 : 24">
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
          <el-form-item label="状态：" prop="status">
            <el-select
              v-model="form.status"
              placeholder="请选择状态"
              clearable
              class="!w-[180px]"
            >
              <el-option label="已上架" :value="true" />
              <el-option label="已下架" :value="false" />
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
            <el-button
              :icon="useRenderIcon(Refresh)"
              @click="resetForm(formRef)"
            >
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="2" :min-width="200" v-if="hasAuth('btn_add')">
        <el-button
          class="custom-button"
          type="primary"
          :icon="useRenderIcon(AddFill)"
          @click="onAddApp"
        >
          新增
        </el-button>
      </el-col>
    </el-row>

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
              pagename="store"
              @install-app="handleInstallApp"
              @revision-app="handleRevisionApp"
              @edit-app="handleEditApp"
              @disable-app="handleDisableApp"
              @enable-app="handleEnableApp"
              @delete-app="handleDeleteApp"
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
        <el-form-item label="仓库地址" prop="url">
          <el-input
            v-model="appForm.url"
            clearable
            placeholder="请输入svn/git仓库地址"
          />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select
            v-model="appForm.category_id"
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
        <el-form-item label="是否发布" prop="status">
          <el-select v-model="appForm.status" placeholder="请选择状态">
            <el-option label="上架" :value="true" />
            <el-option label="下架" :value="false" />
          </el-select>
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
./utils/hookStore
