import { PERMISSION_VEX_DELETE, PERMISSION_VEX_EDIT } from "../access_control/types";
import { is_superuser } from "../commons/functions";

export const update_permission = (csaf: any) => {
    return csaf && (csaf?.product_data?.permissions?.includes(PERMISSION_VEX_EDIT) || is_superuser());
};

export const delete_permission = (csaf: any) => {
    return csaf && (csaf?.product_data?.permissions?.includes(PERMISSION_VEX_DELETE) || is_superuser());
};
