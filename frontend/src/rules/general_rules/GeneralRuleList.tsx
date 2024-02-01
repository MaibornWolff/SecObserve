import { Fragment } from "react";
import {
    BooleanField,
    BulkDeleteButton,
    CreateButton,
    Datagrid,
    List,
    ReferenceField,
    ReferenceInput,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/settings/functions";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
];

const BulkActionButtons = () => {
    const user = localStorage.getItem("user");
    return (
        <Fragment>{user && JSON.parse(user).is_superuser && <BulkDeleteButton mutationMode="pessimistic" />}</Fragment>
    );
};

const ListActions = () => {
    const user = localStorage.getItem("user");
    return <TopToolbar>{user && JSON.parse(user).is_superuser && <CreateButton />}</TopToolbar>;
};

const GeneralRuleList = () => {
    const user = localStorage.getItem("user");
    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={<ListActions />}
            disableSyncWithLocation={false}
            storeKey="general_rules.list"
        >
            <Datagrid
                size={getSettingListSize()}
                rowClick="show"
                bulkActionButtons={user && JSON.parse(user).is_superuser && <BulkActionButtons />}
            >
                <TextField source="name" />
                <TextField source="new_severity" />
                <TextField source="new_status" />
                <BooleanField source="enabled" />
                <ReferenceField source="parser" reference="parsers" link={false} />
                <TextField source="scanner_prefix" />
                <TextField source="title" label="Observation title" />
            </Datagrid>
        </List>
    );
};

export default GeneralRuleList;
