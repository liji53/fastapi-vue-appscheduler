<script setup lang="ts">
import { useWindowSize } from "@vueuse/core";
import { onMounted } from "vue";
import { initSysResource } from "./utils/hookSysResource";

defineOptions({
  name: "Welcome"
});

const { height } = useWindowSize();

onMounted(() => {
  const cpuDom = document.getElementById("cpuDom");
  const memoryDom = document.getElementById("memoryDom");
  const diskDom = document.getElementById("diskDom");
  initSysResource(cpuDom, memoryDom, diskDom);
  // setInterval(setValue, 5000);  // 实时获取
});
</script>

<template>
  <div>
    <el-row :gutter="24">
      <el-col
        :xs="24"
        :sm="24"
        :md="12"
        :lg="12"
        :xl="12"
        class="mb-[18px]"
        v-motion
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 200
          }
        }"
      >
        <el-card
          header="统计"
          shadow="never"
          :style="{ height: `calc(${height}px - 35vh - 250px)` }"
        >
          <div>待实现</div>
        </el-card>
      </el-col>

      <el-col
        :xs="24"
        :sm="24"
        :md="12"
        :lg="12"
        :xl="12"
        class="mb-[18px]"
        v-motion
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 200
          }
        }"
      >
        <el-card
          header="系统资源"
          shadow="never"
          :style="{ height: `calc(${height}px - 35vh - 250px)` }"
        >
          <el-row :gutter="24">
            <el-col :span="8">
              <span id="cpuDom" style="width: 200px; height: 200px" />
            </el-col>
            <el-col :span="8">
              <span id="memoryDom" style="width: 200px; height: 200px" />
            </el-col>
            <el-col :span="8">
              <span id="diskDom" style="width: 200px; height: 200px" />
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <el-col
        :xs="24"
        :sm="24"
        :md="12"
        :lg="8"
        :xl="8"
        class="mb-[18px]"
        v-motion
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 400
          }
        }"
      >
        <el-card header="xx" shadow="never">
          <div>待实现</div>
        </el-card>
      </el-col>

      <el-col
        :xs="24"
        :sm="24"
        :md="12"
        :lg="8"
        :xl="8"
        class="mb-[18px]"
        v-motion
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 400
          }
        }"
      >
        <el-card header="yy" shadow="never">
          <div>待实现</div>
        </el-card>
      </el-col>

      <el-col
        :xs="24"
        :sm="24"
        :md="24"
        :lg="8"
        :xl="8"
        class="mb-[18px]"
        v-motion
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 400
          }
        }"
      >
        <el-card header="zz" shadow="never">
          <div>待实现</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
