<script setup lang="ts">
import { ref, Ref, computed } from "vue";
// import { noticesData } from "./data";
import NoticeList from "./noticeList.vue";
import { TabItem } from "@/api/notice";
import Bell from "@iconify-icons/ep/bell";
import { ElNotification } from "element-plus";
import { listen } from "@tauri-apps/api/event";

const notices: Ref<TabItem[]> = ref([]);

listen("run_app_result", (event: any) => {
  const msg: TabItem = event.payload;
  let is_exists = false;
  notices.value.forEach(item => {
    if (item.name === msg.name) {
      is_exists = true;
      for (const message of msg.list) {
        item.list.push(message);
      }
    }
  });
  if (!is_exists) {
    notices.value.push(msg);
  }
  for (const message of msg.list) {
    ElNotification({
      title: message.title,
      type: message.status === "danger" ? "error" : message.status,
      message: message.description
    });
  }
});

const noticesNum = computed(() => {
  let count = 0;
  for (const v of notices.value) {
    count += v.list.length;
  }
  return count;
});
</script>

<template>
  <el-dropdown trigger="click" placement="bottom-end">
    <span class="dropdown-badge navbar-bg-hover select-none">
      <el-badge :value="noticesNum" :max="99">
        <span class="header-notice-icon">
          <IconifyIconOffline :icon="Bell" />
        </span>
      </el-badge>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-tabs
          :stretch="true"
          class="dropdown-tabs"
          :style="{ width: notices.length === 0 ? '200px' : '330px' }"
        >
          <el-empty
            v-if="notices.length === 0"
            description="暂无消息"
            :image-size="60"
          />
          <span v-else>
            <template v-for="(item, idx) in notices" :key="idx">
              <el-tab-pane :label="`${item.name}(${item.list.length})`">
                <el-scrollbar max-height="330px">
                  <div class="noticeList-container">
                    <NoticeList v-model:list="item.list" />
                  </div>
                </el-scrollbar>
              </el-tab-pane>
            </template>
          </span>
        </el-tabs>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style lang="scss" scoped>
.dropdown-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 48px;
  margin-right: 10px;
  cursor: pointer;

  .header-notice-icon {
    font-size: 18px;
  }
}

.dropdown-tabs {
  .noticeList-container {
    padding: 15px 24px 0;
  }

  :deep(.el-tabs__header) {
    margin: 0;
  }

  :deep(.el-tabs__nav-wrap)::after {
    height: 1px;
  }

  :deep(.el-tabs__nav-wrap) {
    padding: 0 36px;
  }
}
</style>
