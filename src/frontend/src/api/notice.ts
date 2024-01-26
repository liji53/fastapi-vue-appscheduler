export interface ListItem {
  avatar: string;
  title: string;
  datetime: string;
  type: string;
  description: string;
  status: "" | "success" | "warning" | "info" | "danger";
  extra?: string;
}

export interface TabItem {
  name: string;
  list: ListItem[];
}

export interface Log {
  status: boolean;
  execute_type: string;
  content: string;
  task_id: number;
}

export interface RunAppPayload {
  notice: TabItem;
  log: Log;
}
