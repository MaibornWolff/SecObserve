import { Stack } from "@mui/material";
import {
    Datagrid,
    Identifier,
    ListContextProvider,
    ResourceContextProvider,
    SelectField,
    WithRecord,
    useListController,
} from "react-admin";

import {
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_DELETE,
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_EDIT,
    ROLE_CHOICES,
} from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { getSettingListSize } from "../../commons/user_settings/functions";
import ProductAuthorizationGroupMemberDelete from "./ProductAuthorizationGroupMemberDelete";
import ProductAuthorizationGroupMemberEdit from "./ProductAuthorizationGroupMemberEdit";

type ProductAuthorizationGroupMemberEmbeddedListProps = {
    product: any;
};

const showAuthorizationGroup = (id: Identifier) => {
    return "#/authorization_groups/" + id + "/show";
};

const ProductAuthorizationGroupMemberEmbeddedList = ({ product }: ProductAuthorizationGroupMemberEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "product_authorization_group_members",
        sort: { field: "authorization_group_data.name", order: "ASC" },
        disableSyncWithLocation: true,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="product_authorization_group_members">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                        rowClick={false}
                        resource="product_authorization_group_members"
                    >
                        <WithRecord
                            label="Authorization Group"
                            render={(product_authorization_group_member) => (
                                <TextUrlField
                                    label="User"
                                    text={product_authorization_group_member.authorization_group_data.name}
                                    url={showAuthorizationGroup(
                                        product_authorization_group_member.authorization_group_data.id
                                    )}
                                />
                            )}
                        />
                        <SelectField source="role" choices={ROLE_CHOICES} />
                        <WithRecord
                            render={(product_authorization_group_member) => (
                                <Stack direction="row" spacing={4}>
                                    {product?.permissions.includes(
                                        PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_EDIT
                                    ) && <ProductAuthorizationGroupMemberEdit />}
                                    {product?.permissions.includes(
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
        </ResourceContextProvider>
    );
};

export default ProductAuthorizationGroupMemberEmbeddedList;
