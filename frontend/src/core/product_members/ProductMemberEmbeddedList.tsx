import { Stack } from "@mui/material";
import { Datagrid, Identifier, ListContextProvider, SelectField, WithRecord, useListController } from "react-admin";

import {
    PERMISSION_PRODUCT_MEMBER_DELETE,
    PERMISSION_PRODUCT_MEMBER_EDIT,
    ROLE_CHOICES,
} from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { getSettingListSize } from "../../commons/user_settings/functions";
import ProductMemberDelete from "./ProductMemberDelete";
import ProductMemberEdit from "./ProductMemberEdit";

type ProductMemberEmbeddedListProps = {
    product: any;
};

const showUser = (id: Identifier) => {
    return "#/users/" + id + "/show";
};

const ProductMemberEmbeddedList = ({ product }: ProductMemberEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "product_members",
        sort: { field: "user_data.full_name", order: "ASC" },
        disableSyncWithLocation: true,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Datagrid
                    size={getSettingListSize()}
                    sx={{ width: "100%" }}
                    bulkActionButtons={false}
                    rowClick={false}
                    resource="product_members"
                >
                    <WithRecord
                        label="User"
                        render={(product_member) => (
                            <TextUrlField
                                label="User"
                                text={product_member.user_data.full_name}
                                url={showUser(product_member.user_data.id)}
                            />
                        )}
                    />
                    <SelectField source="role" choices={ROLE_CHOICES} />
                    <WithRecord
                        render={(product_member) => (
                            <Stack direction="row" spacing={4}>
                                {product && product.permissions.includes(PERMISSION_PRODUCT_MEMBER_EDIT) && (
                                    <ProductMemberEdit />
                                )}
                                {product && product.permissions.includes(PERMISSION_PRODUCT_MEMBER_DELETE) && (
                                    <ProductMemberDelete product_member={product_member} />
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

export default ProductMemberEmbeddedList;
