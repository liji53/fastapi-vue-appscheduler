<script setup lang="ts">
import { ref, onMounted, watchEffect } from "vue";
import { getAppList } from "@/api/app";
import { getAppCategory } from "@/api/app_category";
import AppCard from "./components/AppCard.vue";
import AppHeader from "./components/AppHeader.vue";

defineOptions({
  name: "Store"
});

const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `;

const apps = ref([]);
const appCategories = ref([]);
const appStatuses = ref(["废弃", "未安装", "已安装", "已上线"]);
const pagination = ref({ current: 1, pageSize: 12, total: 0 });
const dataLoading = ref(true);

const appQueryParams = ref({
  page: 1,
  itemsPerPage: pagination.value.pageSize,
  name: null,
  categoryId: -1,
  statuses: []
});

// api请求
const getAppListData = async (params?: object) => {
  try {
    const response = await getAppList(params);
    apps.value = response.data;
    pagination.value = {
      ...pagination.value,
      total: response.total
    };
  } catch (e) {
    console.log(e);
  } finally {
    setTimeout(() => {
      dataLoading.value = false;
    }, 500);
  }
};
const getAppCategoryData = async () => {
  try {
    const response = await getAppCategory();
    appCategories.value = response.data;
  } catch (e) {
    console.log(e);
  }
};

watchEffect(async () => {
  await getAppListData(appQueryParams.value);
});

onMounted(() => {
  // getAppListData({ page: 1, items_per_page: pagination.value.pageSize });  # 在watchEffect中响应
  getAppCategoryData();
});

// 用于响应AppHeader的事件
const handleSelectAppCategory = async (category_id: number) => {
  pagination.value.current = 1;
  appQueryParams.value.page = 1;
  appQueryParams.value.categoryId = category_id;
};
const handleSelectAppStatus = async (statuses: Array<String>) => {
  pagination.value.current = 1;
  appQueryParams.value.page = 1;
  appQueryParams.value.statuses = statuses;
};
const handleSearchAppName = async (app_name: string) => {
  pagination.value.current = 1;
  appQueryParams.value.page = 1;
  appQueryParams.value.name = app_name;
};

// 用于响应AppCard的事件
const handleInstallApp = (app_id: number) => {
  console.log(app_id);
};
const handleUninstallApp = (app_id: number) => {
  console.log(app_id);
};

// 用于响应分页事件
const onPageSizeChange = (size: number) => {
  pagination.value.pageSize = size;
  pagination.value.current = 1;
  appQueryParams.value.itemsPerPage = size;
  appQueryParams.value.page = 1;
};
const onCurrentPageChange = (current: number) => {
  pagination.value.current = current;
  appQueryParams.value.page = current;
};
</script>

<template>
  <el-card shadow="never">
    <!-- Header -->
    <div class="w-full flex justify-between mb-4">
      <AppHeader
        :categories="appCategories"
        :statuses="appStatuses"
        @select-category="handleSelectAppCategory"
        @select-status="handleSelectAppStatus"
        @search-app="handleSearchAppName"
      >
        后台会自动检测已发布的app，用户需要先安装再使用。
      </AppHeader>
    </div>

    <!-- Body -->
    <div
      v-loading="dataLoading"
      :element-loading-svg="svg"
      element-loading-svg-view-box="-10, -10, 50, 50"
    >
      <el-empty description="暂无数据" v-show="pagination.total === 0" />
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
              @install-app="handleInstallApp"
              @uninstall-app="handleUninstallApp"
            />
          </el-col>
        </el-row>

        <el-pagination
          class="float-right"
          v-model:currentPage="pagination.current"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[12, 24, 36]"
          :background="true"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="onPageSizeChange"
          @current-change="onCurrentPageChange"
        />
      </template>
    </div>
  </el-card>
</template>
