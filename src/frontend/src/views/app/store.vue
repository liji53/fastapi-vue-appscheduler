<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { getAppList } from "@/api/app";
import { appCategory } from "./components/category";
import Card from "./components/Card.vue";
import Search from "@iconify-icons/ep/search";

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

const selected = ref(0);
const pagination = ref({ current: 1, pageSize: 12, total: 0 });
const appList = ref([]);
const dataLoading = ref(true);
const formData = ref({});

const searchValue = ref("");
const formDialogVisible = ref(false);

const getCardListData = async () => {
  try {
    const { data } = await getAppList();
    appList.value = data.list;
    pagination.value = {
      ...pagination.value,
      total: data.list.length
    };
  } catch (e) {
    console.log(e);
  } finally {
    setTimeout(() => {
      dataLoading.value = false;
    }, 500);
  }
};
onMounted(() => {
  getCardListData();
});
const onPageSizeChange = (size: number) => {
  pagination.value.pageSize = size;
  pagination.value.current = 1;
};
const onCurrentChange = (current: number) => {
  pagination.value.current = current;
};

function tabClick({ index }) {
  selected.value = index;
}
const handleInstallApp = app => {
  console.log("download app" + app.name);
};
const handleInfoApp = app => {
  formDialogVisible.value = true;
  nextTick(() => {
    formData.value = { ...app };
  });
};
</script>

<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <div class="w-full flex justify-between mb-4">
          <span class="font-medium">
            应用商城会自动检测后台app，只要svn上传app之后，商城会自动上架该app，用户需要先安装再使用。
          </span>
          <el-input
            style="width: 300px"
            v-model="searchValue"
            placeholder="请输入应用名称"
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
      </div>
    </template>

    <el-tabs @tab-click="tabClick">
      <template v-for="item of appCategory" :key="item.key">
        <el-tab-pane :lazy="true">
          <template #label>
            <el-tooltip :content="item.content" placement="top-end">
              <span>{{ item.title }}</span>
            </el-tooltip>
          </template>
          <div
            v-loading="dataLoading"
            :element-loading-svg="svg"
            element-loading-svg-view-box="-10, -10, 50, 50"
          >
            <el-empty
              description="暂无数据"
              v-show="
                appList
                  .slice(
                    pagination.pageSize * (pagination.current - 1),
                    pagination.pageSize * pagination.current
                  )
                  .filter(v =>
                    v.name.toLowerCase().includes(searchValue.toLowerCase())
                  ).length === 0
              "
            />
            <template v-if="pagination.total > 0">
              <el-row :gutter="16">
                <el-col
                  v-for="(app, index) in appList
                    .slice(
                      pagination.pageSize * (pagination.current - 1),
                      pagination.pageSize * pagination.current
                    )
                    .filter(v =>
                      v.name.toLowerCase().includes(searchValue.toLowerCase())
                    )"
                  :key="index"
                  :xs="24"
                  :sm="12"
                  :md="8"
                  :lg="6"
                  :xl="4"
                >
                  <Card
                    :app="app"
                    @install-app="handleInstallApp"
                    @info-app="handleInfoApp"
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
                @current-change="onCurrentChange"
              />
            </template>
          </div>
          <el-dialog v-model="formDialogVisible" title="详情信息">
            <span>{{ formData["name"] }}</span>
          </el-dialog>
        </el-tab-pane>
      </template>
    </el-tabs>
  </el-card>
</template>
