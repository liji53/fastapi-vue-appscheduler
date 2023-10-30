interface FormItemProps {
  id?: number;
  /** 用于判断是`新增`还是`修改` */
  title: string;
  username: string;
  password: string;
  phone: string | number;
  email: string;
  status: boolean;
  remark: string;
}
interface FormProps {
  formInline: FormItemProps;
}

interface RoleFormItemProps {
  user_id: number;
  username: string;
  /** 角色列表 */
  roleOptions: any[];
  /** 选中的角色列表 */
  ids: Record<number, unknown>[];
}
interface RoleFormProps {
  formInline: RoleFormItemProps;
}

export type { FormItemProps, FormProps, RoleFormItemProps, RoleFormProps };
