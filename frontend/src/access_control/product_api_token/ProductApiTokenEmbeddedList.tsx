import { Paper } from "@mui/material";
import { Datagrid, ListContextProvider, Pagination, SelectField, useListController } from "react-admin";

import { PERMISSION_PRODUCT_API_TOKEN_REVOKE, ROLE_CHOICES } from "../../access_control/types";
import RevokeProductApiToken from "./ProductApiTokenRevoke";

type ProductApiTokenEmbeddedListProps = {
    product: any;
};

const ProductApiTokenEmbeddedList = ({ product }: ProductApiTokenEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "product_api_tokens";
    const sort = { field: "role", order: "ASC" };
    const disableSyncWithLocation = true;
    const storeKey = "product_api_tokens.embedded";

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
                    <Datagrid size="medium" sx={{ width: "100%" }} bulkActionButtons={false}>
                        <SelectField source="role" choices={ROLE_CHOICES} />
                        {product && product.permissions.includes(PERMISSION_PRODUCT_API_TOKEN_REVOKE) && (
                            <RevokeProductApiToken product={product} />
                        )}
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductApiTokenEmbeddedList;
