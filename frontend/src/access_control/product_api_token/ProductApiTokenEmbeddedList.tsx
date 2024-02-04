import { Datagrid, ListContextProvider, SelectField, useListController } from "react-admin";

import { PERMISSION_PRODUCT_API_TOKEN_REVOKE, ROLE_CHOICES } from "../../access_control/types";
import { getSettingListSize } from "../../commons/settings/functions";
import RevokeProductApiToken from "./ProductApiTokenRevoke";

type ProductApiTokenEmbeddedListProps = {
    product: any;
};

const ProductApiTokenEmbeddedList = ({ product }: ProductApiTokenEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "product_api_tokens",
        sort: { field: "role", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "product_api_tokens.embedded",
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
                    <SelectField source="role" choices={ROLE_CHOICES} />
                    {product && product.permissions.includes(PERMISSION_PRODUCT_API_TOKEN_REVOKE) && (
                        <RevokeProductApiToken product={product} />
                    )}
                </Datagrid>
            </div>
        </ListContextProvider>
    );
};

export default ProductApiTokenEmbeddedList;
