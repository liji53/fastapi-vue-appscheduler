<script setup lang="ts">
import * as echarts from "echarts";
import { onMounted } from "vue";
import { getSystemResource } from "@/api/system_resource";

defineOptions({
  name: "Resource"
});

type EChartsOption = echarts.EChartsOption;

onMounted(() => {
  const cpuDom = document.getElementById("cpuDom");
  const memoryDom = document.getElementById("memoryDom");
  const diskDom = document.getElementById("diskDom");
  const cpuChart = echarts.init(cpuDom);
  const memoryChart = echarts.init(memoryDom);
  const diskChart = echarts.init(diskDom);

  const option: EChartsOption = {
    series: [
      {
        type: "gauge",
        axisLine: {
          lineStyle: {
            width: 30,
            color: [
              [0.3, "#67e0e3"],
              [0.7, "#37a2da"],
              [1, "#fd666d"]
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: "auto"
          }
        },
        axisTick: {
          distance: -30,
          length: 8,
          lineStyle: {
            color: "#fff",
            width: 2
          }
        },
        splitLine: {
          distance: -30,
          length: 30,
          lineStyle: {
            color: "#fff",
            width: 4
          }
        },
        axisLabel: {
          color: "inherit",
          distance: 40,
          fontSize: 15,
          formatter: function (val) {
            return `${Math.ceil(val)}`;
          }
        },
        detail: {
          valueAnimation: true,
          formatter: "{value} %",
          color: "inherit"
        }
      }
    ]
  };

  async function setValue() {
    const res = await getSystemResource();
    cpuChart.setOption<echarts.EChartsOption>({
      series: [{ data: [{ value: res.cpu }] }]
    });
    memoryChart.setOption<echarts.EChartsOption>({
      series: [{ data: [{ value: res.memory }] }]
    });
    diskChart.setOption<echarts.EChartsOption>({
      series: [
        {
          max: res.full_disk,
          data: [{ value: res.disk }],
          detail: {
            valueAnimation: true,
            formatter: "{value} GB",
            color: "inherit"
          }
        }
      ]
    });
  }
  setValue();
  // setInterval(setValue, 5000);

  option && cpuChart.setOption(option);
  option && memoryChart.setOption(option);
  option && diskChart.setOption(option);
});
</script>

<template>
  <el-row :gutter="24">
    <el-col :span="8">
      <el-card header="cpu使用率">
        <div id="cpuDom" style="width: 400px; height: 400px" />
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card header="内存使用率">
        <div id="memoryDom" style="width: 400px; height: 400px" />
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card header="硬盘使用空间">
        <div id="diskDom" style="width: 400px; height: 400px" />
      </el-card>
    </el-col>
  </el-row>
</template>
