import { ref, onMounted } from "vue";
import { getAppTree } from "@/api/app";
import { getAppForm, setAppForm } from "@/api/app_form";

export function useAppForm() {
  const TreeProps = ref({
    value: "id",
    label: "name",
    children: "children"
  });

  const appTree = ref([]);
  const currentApp = ref<number>();

  // 动态表单与现有框架结合使用有问题，因此动态表单额外单独实现，同时砍掉部分基础控件和布局
  const starfishRef = ref();
  // 工作区上方的操作menu
  const lowcodeMenu = ref({
    left: ["undo", "redo", "save", "preview"],
    right: ["json-export", "json-import"],
    column: false
  });
  // 基础控件
  const lowcodeBasicFields = ref([
    "Text",
    "TextArea",
    "Switch",
    "Radio",
    "CheckBox",
    "Date",
    "Time",
    "InputNumber",
    "Slider",
    "Selected",
    "Selecteds"
  ]);
  // 布局控件，全部去掉
  const lowcodeLayoutFields = ref(["?"]);
  // const lowcodeBasicFields = ref([]);

  onMounted(() => {
    getAppTree().then(response => {
      appTree.value = response.data;
    });
  });

  const onLowcodeSave = async (res: any[]) => {
    await setAppForm(currentApp.value, { form: JSON.stringify(res) });
  };

  const handleTreeClick = data => {
    if (!("children" in data) || data["children"] === null) {
      currentApp.value = data.id;
      getAppForm({ app_id: data.id }).then(response => {
        if (response.form != null) {
          starfishRef.value.setJson(JSON.parse(response.form));
        } else {
          starfishRef.value.setJson([]);
        }
      });
    }
  };
  return {
    appTree,
    TreeProps,
    currentApp,
    starfishRef,
    lowcodeMenu,
    lowcodeBasicFields,
    lowcodeLayoutFields,
    onLowcodeSave,
    handleTreeClick
  };
}
