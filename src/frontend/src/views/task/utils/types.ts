interface ProjectItemProps {
  // 主键
  id?: number;
  /** 名称 */
  name: string;
  /** 备注 */
  remark: string;
}
interface ProjectFormProps {
  formInline: ProjectItemProps;
}

interface JobItemProps {
  // 主键
  id?: number;
  /** 任务名称 */
  name: string;
  project_id: number;
  projects: Array<ProjectItemProps>;
  /* 指的是已安装的应用 */
  app_id: number;
  apps: Array<any>;
  /** 备注 */
  remark: string;
}
interface JobFormProps {
  formInline: JobItemProps;
}

export type { ProjectItemProps, ProjectFormProps, JobFormProps, JobItemProps };
