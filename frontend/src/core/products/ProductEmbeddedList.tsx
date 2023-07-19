import { Paper } from "@mui/material";
import {
    Datagrid,
    FilterForm,
    ListContextProvider,
    Pagination,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";

type ProductEmbeddedListProps = {
    product_group: any;
};

const ShowProducts = (id: any) => {
    return "../../../../products/" + id + "/show";
};

function listFilters() {
    return [<TextInput source="name" alwaysOn />];
}

const ProductEmbeddedList = ({ product_group }: ProductEmbeddedListProps) => {
    const filter = { product_group: Number(product_group.id) };
    const perPage = 25;
    const resource = "products";
    const sort = { field: "name", order: "ASC" };
    const filterDefaultValues = {};
    const disableSyncWithLocation = false;
    const storeKey = "products.embedded";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        filterDefaultValues,
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
                <FilterForm filters={listFilters()} />
                <Paper>
                    <Datagrid size="medium" rowClick={ShowProducts} bulkActionButtons={false}>
                        <TextField source="name" />
                        <SecurityGateTextField />
                        <TextField source="repository_default_branch_name" label="Default branch" sortable={false} />
                        <ObservationsCountField withLabel={false} />
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductEmbeddedList;
