import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/appforms/12",
    method: "get",
    response: () => {
      return {
        form: JSON.stringify([
          {
            ControlType: "TextArea",
            nameCn: "文本域",
            id: "fU1ocjKnSLOA3Djmpus1g",
            layout: false,
            data: {
              fieldName: "TextArea_k3Qy8gCo_4FVYDsO7nwS0",
              label: "标签名称",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: "",
              csslist: []
            }
          },
          {
            ControlType: "Text",
            nameCn: "文本框",
            id: "EIJjqJRZqkd92p1JzveGv",
            layout: false,
            data: {
              fieldName: "Text_naX7oUYyKfqOPH8gtHJbg",
              label: "标签名称",
              tip: "",
              placeholder: "",
              showRule: "{}",
              required: false,
              rule: "[]",
              default: ""
            }
          }
        ])
      };
    }
  }
] as MockMethod[];
