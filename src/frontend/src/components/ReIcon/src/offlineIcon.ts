import { addIcon } from "@iconify/vue/dist/offline";

/**
 * 这里存放本地图标，在 src/layout/index.vue 文件中加载，避免在首启动加载
 */

// 本地菜单图标，后端在路由的icon中返回对应的图标字符串并且前端在此处使用addIcon添加即可渲染菜单图标
import HomeFilled from "@iconify-icons/ep/home-filled";
import InformationLine from "@iconify-icons/ri/information-line";
import Menu from "@iconify-icons/ep/menu";
import Monitor from "@iconify-icons/ep/monitor";
import ListCheck from "@iconify-icons/ri/list-check";
import FlUser from "@iconify-icons/ri/admin-line";

addIcon("homeFilled", HomeFilled);
addIcon("informationLine", InformationLine);
addIcon("menu", Menu);
addIcon("monitor", Monitor);
addIcon("listCheck", ListCheck);
addIcon("flUser", FlUser);
