import { defineStore } from "pinia";
import { store } from "@/store";

export const useWebSocketStore = defineStore("webSocket", {
  state: () => ({
    task_socket: null
  }),
  actions: {
    createTaskSocket() {
      // WebSocket连接的URL
      const url = `ws://${window.location.host}/api/v1/tasks/ws`;
      this.task_socket = new WebSocket(url);
    },
    getTaskSocket() {
      if (!this.task_socket) {
        this.createTaskSocket();
      }
      return this.task_socket;
    }
  }
});

export function useWebSocketStoreHook() {
  return useWebSocketStore(store);
}
