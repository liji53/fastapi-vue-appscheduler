<script setup lang="ts">
import { PropType } from "vue";
import { ListItem } from "@/api/notice";
import NoticeItem from "./noticeItem.vue";

const props = defineProps({
  list: {
    type: Array as PropType<Array<ListItem>>,
    default: () => []
  }
});
const emits = defineEmits(["update:list"]);

const onReadDone = (index: number) => {
  // 删除指定下标的元素
  const updatedList = [...props.list];
  updatedList.splice(index, 1);
  emits("update:list", updatedList); // 触发更新 list 的事件，将更新后的数组传递给父组件
};
</script>

<template>
  <div v-if="props.list.length">
    <NoticeItem
      v-for="(item, index) in props.list"
      :noticeItem="item"
      :key="index"
      @read-done="onReadDone(index)"
    />
  </div>
  <el-empty v-else description="暂无数据" />
</template>
