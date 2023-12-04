<script setup lang="ts">
import { useAppForm } from "./utils/hookAppForm";

defineOptions({
  name: "AppForm"
});

const {
  appTree,
  currentApp,
  starfishRef,
  lowcodeMenu,
  lowcodeBasicFields,
  lowcodeLayoutFields,
  TreeProps,
  onLowcodeSave,
  handleTreeClick
} = useAppForm();
</script>

<template>
  <div class="flex justify-between">
    <el-card style="width: 180px">
      <el-tree
        v-modle="currentApp"
        :data="appTree"
        :props="TreeProps"
        accordion
        highlight-current
        @node-click="handleTreeClick"
      />
    </el-card>
    <div class="w-[calc(100%-190px)]">
      <starfish-editor
        :headerShow="false"
        :basicFields="lowcodeBasicFields"
        :layoutFields="lowcodeLayoutFields"
        :menu="lowcodeMenu"
        class="starfish-editor"
        @save="onLowcodeSave"
        ref="starfishRef"
      />
    </div>
  </div>
</template>
