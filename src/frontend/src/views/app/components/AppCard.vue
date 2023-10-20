<script setup lang="ts">
import { ref, computed } from "vue";
import More2Fill from "@iconify-icons/ri/more-2-fill";

const props = defineProps(["app"]);
defineEmits([
  "install-app",
  "revision-app",
  "edit-app",
  "uninstall-app",
  "info-app"
]);

const infoDialogVisible = ref(false);

const isNotUse = computed(
  () => props.app.status === "未安装" || props.app.status === "废弃"
);
const isNotInstall = computed(() => props.app.status === "未安装");

// 卡片的样式
const cardClass = computed(() => [
  "list-card-item",
  {
    "list-card-item__disabled": isNotUse.value
  }
]);
const cardLogoClass = computed(() => [
  "list-card-item_detail--logo",
  {
    "list-card-item_detail--logo__disabled": isNotUse.value
  }
]);
</script>

<template>
  <div :class="cardClass">
    <div class="list-card-item_detail bg-bg_color">
      <!-- logo + 状态 + 操作 -->
      <el-row justify="space-between">
        <div
          :class="cardLogoClass"
          :style="`background-image: url(${app.banner})`"
        />
        <div class="list-card-item_detail--operation">
          <el-tag
            :color="!isNotUse ? '#00a870' : '#eee'"
            effect="dark"
            class="mx-1 list-card-item_detail--operation--tag"
          >
            {{ app.status }}
          </el-tag>
          <el-dropdown trigger="click">
            <IconifyIconOffline :icon="More2Fill" class="text-[24px]" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  v-if="isNotInstall"
                  @click="$emit('install-app', app.id)"
                >
                  安装
                </el-dropdown-item>
                <el-dropdown-item @click="$emit('revision-app', app.id)">
                  版本
                </el-dropdown-item>
                <el-dropdown-item @click="$emit('edit-app', app.id)">
                  编辑
                </el-dropdown-item>
                <el-dropdown-item
                  v-if="!isNotUse"
                  @click="$emit('uninstall-app', app.id)"
                >
                  卸载
                </el-dropdown-item>
                <el-dropdown-item
                  @click="
                    $emit('info-app', app.id);
                    infoDialogVisible = true;
                  "
                >
                  详情
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-row>

      <!-- name -->
      <p class="list-card-item_detail--name text-text_color_primary">
        {{ app.name }}
      </p>

      <p class="list-card-item_detail--desc text-text_color_regular">
        {{ app.description }}
      </p>
    </div>
  </div>

  <!-- dialog -->
  <el-dialog v-model="infoDialogVisible" title="详情信息">
    <span>未支持</span>
  </el-dialog>
</template>

<style scoped lang="scss">
.list-card-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
  overflow: hidden;
  cursor: pointer;
  border-radius: 3px;

  &_detail {
    flex: 1;
    min-height: 140px;
    padding: 24px 32px;

    &--logo {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 56px;
      height: 56px;
      font-size: 32px;
      color: #0052d9;
      background: #e0ebff;
      border-radius: 50%;
      background-size: cover;
      background-position: center;

      &__disabled {
        color: #a1c4ff;
      }
    }

    &--operation {
      display: flex;
      height: 100%;

      &--tag {
        border: 0;
      }
    }

    &--name {
      margin: 24px 0 8px;
      font-size: 16px;
      font-weight: 400;
    }

    &--desc {
      display: -webkit-box;
      height: 40px;
      margin-bottom: 24px;
      overflow: hidden;
      font-size: 12px;
      line-height: 20px;
      text-overflow: ellipsis;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }
  }

  &__disabled {
    .list-card-item_detail--name,
    .list-card-item_detail--desc {
      color: var(--el-text-color-disabled);
    }

    .list-card-item_detail--operation--tag {
      color: #bababa;
    }
  }
}
</style>
