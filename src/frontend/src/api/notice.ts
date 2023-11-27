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
