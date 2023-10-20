<script setup lang="ts">
import { ref } from "vue";
import Search from "@iconify-icons/ep/search";
defineEmits(["search-app", "select-category", "select-status"]);
const props = defineProps(["categories", "statuses"]);

const searchValue = ref("");
const category = ref("0");
const status = ref([]);

const removeAll = () => {
  status.value = [];
};
const selectAll = () => {
  status.value = props.statuses;
};
</script>

<template>
  <slot />

  <!-- 应用类别选择 -->
  <el-select v-model="category" @change="$emit('select-category', category)">
    <el-option label="全部分类" value="0" />
    <template v-for="item of categories" :key="item.id">
      <el-tooltip :content="item.description" placement="right">
        <el-option :label="item.name" :value="item.id" />
      </el-tooltip>
    </template>
  </el-select>

  <!-- 状态选择 -->
  <el-select v-model="status" multiple collapse-tags>
    <template #prefix> 状态 </template>
    <div>
      <el-option
        v-for="status_name of statuses"
        :key="status_name"
        :label="status_name"
        :value="status_name"
      />
    </div>
    <div>
      <el-button @click="selectAll">全选</el-button>
      <el-button @click="removeAll">清空</el-button>
      <el-button @click="$emit('select-status', status)" type="primary"
        >确定</el-button
      >
    </div>
  </el-select>

  <!-- 搜索框 -->
  <el-input
    style="width: 300px"
    v-model="searchValue"
    placeholder="请输入应用名称"
    clearable
    @change="$emit('search-app', searchValue)"
  >
    <template #suffix>
      <el-icon class="el-input__icon">
        <IconifyIconOffline v-show="searchValue.length === 0" :icon="Search" />
      </el-icon>
    </template>
  </el-input>
</template>
