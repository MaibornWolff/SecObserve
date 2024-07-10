import {
    ChipField,
    Datagrid,
    FilterForm,
    ListContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { VEX_STATUS_CHOICES } from "../types";

const ShowVEXStatement = (id: any) => {
    return "../../../../vex/vex_statements/" + id + "/show";
};

function listFilters() {
    return [
        <TextInput source="vulnerability_id" label="Vulnerability ID" alwaysOn />,
        <AutocompleteInputMedium source="status" choices={VEX_STATUS_CHOICES} alwaysOn />,
    ];
}

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

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters()} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={ShowVEXStatement}
                    bulkActionButtons={false}
                    resource="vex/vex_statements"
                >
                    <TextField source="vulnerability_id" label="Vulnerability ID" />
                    <ChipField source="status" />
                    <TextField source="product_purl" label="Product" />
                    <TextField source="component_purl" label="Component" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default VEXStatementEmbeddedList;
