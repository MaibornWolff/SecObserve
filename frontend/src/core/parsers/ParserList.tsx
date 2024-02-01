import { AutocompleteInput, Datagrid, List, TextField, TextInput } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/settings/functions";
import { PARSER_SOURCE_CHOICES, SCANNER_TYPE_CHOICES } from "../types";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <AutocompleteInput source="type" choices={SCANNER_TYPE_CHOICES} alwaysOn />,
    <AutocompleteInput source="source" choices={PARSER_SOURCE_CHOICES} alwaysOn />,
];

const ParserList = () => {
    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={false}
            disableSyncWithLocation={false}
        >
            <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false}>
                <TextField source="name" />
                <TextField source="type" />
                <TextField source="source" />
            </Datagrid>
        </List>
    );
};

export default ParserList;
