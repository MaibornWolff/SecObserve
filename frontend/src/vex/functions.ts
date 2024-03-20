import { PERMISSION_VEX_DELETE, PERMISSION_VEX_EDIT } from "../access_control/types";

export const update_permission = (csaf: any | null) => {
    const user = localStorage.getItem("user");
    return (
        csaf &&
        ((csaf.product_data &&
            csaf.product_data.permissions &&
            csaf.product_data.permissions.includes(PERMISSION_VEX_EDIT)) ||
            (user && (csaf.user == JSON.parse(user).id || JSON.parse(user).is_superuser)))
    );
};

export const delete_permission = (csaf: any | null) => {
    const user = localStorage.getItem("user");
    return (
        csaf &&
        ((csaf.product_data &&
            csaf.product_data.permissions &&
            csaf.product_data.permissions.includes(PERMISSION_VEX_DELETE)) ||
            (user && (csaf.user == JSON.parse(user).id || JSON.parse(user).is_superuser)))
    );
};
