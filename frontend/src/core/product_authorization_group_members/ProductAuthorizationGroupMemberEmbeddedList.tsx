import { Stack } from "@mui/material";
import { Datagrid, ListContextProvider, SelectField, TextField, WithRecord, useListController } from "react-admin";

import {
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_DELETE,
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_EDIT,
    ROLE_CHOICES,
} from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";
import ProductAuthorizationGroupMemberDelete from "./ProductAuthorizationGroupMemberDelete";
import ProductAuthorizationGroupMemberEdit from "./ProductAuthorizationGroupMemberEdit";

type ProductAuthorizationGroupMemberEmbeddedListProps = {
    product: any;
};

const ProductAuthorizationGroupMemberEmbeddedList = ({ product }: ProductAuthorizationGroupMemberEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "product_authorization_group_members",
        sort: { field: "authorization_group_name", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "product_authorization_group_member.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Datagrid size={getSettingListSize()} sx={{ width: "100%" }} bulkActionButtons={false}>
                    <TextField source="authorization_group_name" label="Authorization Group" />
                    <SelectField source="role" choices={ROLE_CHOICES} />
                    <WithRecord
                        render={(product_authorization_group_member) => (
                            <Stack direction="row" spacing={4}>
                                {product &&
                                    product.permissions.includes(
                                        PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_EDIT
                                    ) && <ProductAuthorizationGroupMemberEdit />}
                                {product &&
                                    product.permissions.includes(
                                        PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_DELETE
                                    ) && (
                                        <ProductAuthorizationGroupMemberDelete
                                            product_authorization_group_member={product_authorization_group_member}
                                        />
                                    )}
                            </Stack>
                        )}
                    />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductAuthorizationGroupMemberEmbeddedList;
