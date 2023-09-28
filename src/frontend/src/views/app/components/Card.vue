<script setup lang="ts">
import { computed, PropType } from "vue";
import shopIcon from "@/assets/svg/shop.svg?component";
import laptopIcon from "@/assets/svg/laptop.svg?component";
import serviceIcon from "@/assets/svg/service.svg?component";
import calendarIcon from "@/assets/svg/calendar.svg?component";
import userAvatarIcon from "@/assets/svg/user_avatar.svg?component";
import More2Fill from "@iconify-icons/ri/more-2-fill";

defineOptions({
  name: "ReCard"
});

interface CardAppType {
  type: number;
  isInstall: boolean;
  isOnline?: boolean;
  description: string;
  name: string;
}

const props = defineProps({
  app: {
    type: Object as PropType<CardAppType>
  },
  manager: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits([
  "install-app",
  "change-version",
  "edit-app",
  "delete-app",
  "info-app"
]);

const handleClickInstall = (app: CardAppType) => {
  emit("install-app", app);
};

const handleClickChange = (app: CardAppType) => {
  emit("change-version", app);
};

const handleClickEdit = (app: CardAppType) => {
  emit("edit-app", app);
};

const handleClickDelete = (app: CardAppType) => {
  emit("delete-app", app);
};

const handleClickInfo = (app: CardAppType) => {
  emit("info-app", app);
};

const cardClass = computed(() => [
  "list-card-item",
  {
    "list-card-item__disabled": props.manager
      ? !props.app.isOnline
      : !props.app.isInstall
  }
]);

const cardLogoClass = computed(() => [
  "list-card-item_detail--logo",
  {
    "list-card-item_detail--logo__disabled": props.manager
      ? !props.app.isOnline
      : !props.app.isInstall
  }
]);
</script>

<template>
  <div :class="cardClass">
    <div class="list-card-item_detail bg-bg_color">
      <el-row justify="space-between">
        <div :class="cardLogoClass">
          <shopIcon v-if="app.type === 1" />
          <calendarIcon v-if="app.type === 2" />
          <serviceIcon v-if="app.type === 3" />
          <userAvatarIcon v-if="app.type === 4" />
          <laptopIcon v-if="app.type === 5" />
        </div>
        <div class="list-card-item_detail--operation">
          <el-tag
            :color="
              (manager ? app.isOnline : app.isInstall) ? '#00a870' : '#eee'
            "
            effect="dark"
            class="mx-1 list-card-item_detail--operation--tag"
          >
            {{
              manager
                ? app.isOnline
                  ? "已上线"
                  : "未上线"
                : app.isInstall
                ? "已安装"
                : "未安装"
            }}
          </el-tag>
          <el-dropdown trigger="click">
            <IconifyIconOffline :icon="More2Fill" class="text-[24px]" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  v-if="!app.isInstall"
                  @click="handleClickInstall(app)"
                >
                  安装
                </el-dropdown-item>
                <el-dropdown-item
                  v-if="manager"
                  @click="handleClickChange(app)"
                >
                  版本
                </el-dropdown-item>
                <el-dropdown-item v-if="manager" @click="handleClickEdit(app)">
                  编辑
                </el-dropdown-item>
                <el-dropdown-item
                  v-if="manager"
                  @click="handleClickDelete(app)"
                >
                  删除
                </el-dropdown-item>
                <el-dropdown-item @click="handleClickInfo(app)">
                  详情
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-row>
      <p class="list-card-item_detail--name text-text_color_primary">
        {{ app.name }}
      </p>
      <p class="list-card-item_detail--desc text-text_color_regular">
        {{ app.description }}
      </p>
    </div>
  </div>
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
