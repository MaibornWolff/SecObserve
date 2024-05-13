import {
    ChipField,
    Datagrid,
    FilterForm,
    FunctionField,
    ListContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";

const ShowVEXStatement = (id: any) => {
    return "../../../../vex/vex_statements/" + id + "/show";
};

function listFilters() {
    return [<TextInput source="vulnerability_id" alwaysOn />];
}

const get_product = (vex_statement: any | undefined) => {
    if (!vex_statement) {
        return "";
    }

    if (vex_statement.product_purl) {
        return vex_statement.product_purl;
    } else if (vex_statement.product_cpe23) {
        return vex_statement.product_cpe23;
    } else if (vex_statement.product_id) {
        return vex_statement.product_id;
    }

    return "";
};

const get_component = (vex_statement: any | undefined) => {
    if (!vex_statement) {
        return "";
    }

    if (vex_statement.component_purl) {
        return vex_statement.component_purl;
    } else if (vex_statement.component_cpe23) {
        return vex_statement.component_cpe23;
    } else if (vex_statement.component_id) {
        return vex_statement.component_id;
    }

    return "";
};

type VEXStatementEmbeddedListProps = {
    vex_document: any;
};

const VEXStatementEmbeddedList = ({ vex_document }: VEXStatementEmbeddedListProps) => {
    const listContext = useListController({
        filter: { document: Number(vex_document.id) },
        perPage: 25,
        resource: "vex/vex_statements",
        sort: { field: "vulnerability_id", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: "vex_statements.embedded",
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
                <Datagrid size={getSettingListSize()} rowClick={ShowVEXStatement} bulkActionButtons={false}>
                    <TextField source="vulnerability_id" label="Vulnerability ID" />
                    <ChipField source="status" />
                    <FunctionField label="Product" render={(record: any) => get_product(record)} />
                    <FunctionField label="Component" render={(record: any) => get_component(record)} />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default VEXStatementEmbeddedList;
