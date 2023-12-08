import { getSystemResource } from "@/api/system_resource";
import * as echarts from "echarts";

type EChartsOption = echarts.EChartsOption;

export async function initSysResource(cpuDom, memoryDom, diskDom) {
  const option: EChartsOption = {
    title: {
      text: "",
      textStyle: {
        color: "#333", // 标题颜色
        fontSize: 15, // 标题字号
        fontWeight: "normal" // 标题字重
      }
    },
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
          distance: -25,
          fontSize: 15,
          formatter: function (val) {
            return `${Math.ceil(val)}`;
          }
        },
        detail: {
          fontSize: 15,
          valueAnimation: true,
          formatter: "{value} %",
          color: "inherit"
        }
      }
    ]
  };
  const cpuChart = echarts.init(cpuDom);
  const memoryChart = echarts.init(memoryDom);
  const diskChart = echarts.init(diskDom);

  option && cpuChart.setOption(option);
  option && memoryChart.setOption(option);
  option && diskChart.setOption(option);

  const res = await getSystemResource();
  cpuChart.setOption<echarts.EChartsOption>({
    title: { text: "cpu" },
    series: [{ data: [{ value: res.cpu }] }]
  });
  memoryChart.setOption<echarts.EChartsOption>({
    title: { text: "内存" },
    series: [{ data: [{ value: res.memory }] }]
  });
  diskChart.setOption<echarts.EChartsOption>({
    title: { text: "磁盘" },
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
