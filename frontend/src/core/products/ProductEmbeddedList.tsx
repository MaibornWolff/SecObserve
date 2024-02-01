import {
    Datagrid,
    FilterForm,
    FunctionField,
    ListContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { humanReadableDate } from "../../commons/functions";
import { getSettingListSize } from "../../commons/settings/functions";
import { Product } from "../types";

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
    const listContext = useListController({
        filter: { product_group: Number(product_group.id) },
        perPage: 25,
        resource: "products",
        sort: { field: "name", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: false,
        storeKey: "products.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    localStorage.setItem("productembeddedlist.product_group", product_group.id);

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} rowClick={ShowProducts} bulkActionButtons={false}>
                    <TextField source="name" />
                    <TextField source="repository_default_branch_name" label="Default branch" sortable={false} />
                    <SecurityGateTextField />
                    <ObservationsCountField withLabel={false} />
                    <FunctionField<Product>
                        label="Last observation change"
                        sortBy="last_observation_change"
                        render={(record) => (record ? humanReadableDate(record.last_observation_change) : "")}
                    />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductEmbeddedList;
