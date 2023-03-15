import {
    useListController,
    Datagrid,
    TextField,
    ListContextProvider,
    Pagination,
    SelectField,
    WithRecord,
} from "react-admin";
import { Paper, Stack } from "@mui/material";

import {
    PERMISSION_PRODUCT_MEMBER_DELETE,
    PERMISSION_PRODUCT_MEMBER_EDIT,
    ROLE_CHOICES,
} from "../../access_control/types";
import ProductMemberDelete from "./ProductMemberDelete";
import ProductMemberEdit from "./ProductMemberEdit";

type ProductMemberEmbeddedListProps = {
    product: any;
};

const ProductMemberEmbeddedList = ({
    product,
}: ProductMemberEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "product_members";
    const sort = { field: "user_data.full_name", order: "ASC" };
    const disableSyncWithLocation = true;
    const storeKey = "product_member.embedded";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        disableSyncWithLocation,
        storeKey,
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
                <Paper>
                    <Datagrid
                        size="medium"
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                    >
                        <TextField source="user_data.full_name" label="User" />
                        <SelectField source="role" choices={ROLE_CHOICES} />
                        <WithRecord
                            render={(product_member) => (
                                <Stack direction="row" spacing={4}>
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_MEMBER_EDIT
                                        ) && <ProductMemberEdit />}
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_MEMBER_DELETE
                                        ) && (
                                            <ProductMemberDelete
                                                product_member={product_member}
                                            />
                                        )}
                                </Stack>
                            )}
                        />
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductMemberEmbeddedList;
