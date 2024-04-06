import { Datagrid, FilterForm, ListContextProvider, TextField, TextInput, useListController } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/settings/functions";

function listFilters() {
    return [<TextInput source="name" id="api_token_name" alwaysOn />];
}

const ApiTokenEmbeddedList = () => {
    const listContext = useListController({
        filter: {},
        perPage: 25,
        resource: "api_tokens",
        sort: { field: "name", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: false,
        storeKey: "api_tokens.embedded",
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
                <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false}>
                    <TextField source="name" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ApiTokenEmbeddedList;
