import { Fragment } from "react";
import {
    BooleanField,
    BulkDeleteButton,
    ChipField,
    CreateButton,
    Datagrid,
    List,
    ReferenceField,
    ReferenceInput,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import general_rules from ".";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { is_superuser } from "../../commons/functions";
import { feature_general_rules_need_approval_enabled } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { RULE_STATUS_CHOICES } from "../types";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
];
if (feature_general_rules_need_approval_enabled()) {
    listFilters.push(
        <AutocompleteInputMedium
            source="approval_status"
            choices={RULE_STATUS_CHOICES}
            label="Approval status"
            alwaysOn
        />
    );
}

const BulkActionButtons = () => {
    return <Fragment>{is_superuser() && <BulkDeleteButton mutationMode="pessimistic" />}</Fragment>;
};

const ListActions = () => {
    return <TopToolbar>{is_superuser() && <CreateButton />}</TopToolbar>;
};

const GeneralRuleList = () => {
    return (
        <Fragment>
            <ListHeader icon={general_rules.icon} title="General Rules" />
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
                    bulkActionButtons={is_superuser() && <BulkActionButtons />}
                >
                    <TextField source="name" />
                    <TextField source="new_severity" />
                    <TextField source="new_status" />
                    {feature_general_rules_need_approval_enabled() && <ChipField source="approval_status" />}
                    <BooleanField source="enabled" />
                    <ReferenceField source="parser" reference="parsers" link={false} />
                    <TextField source="scanner_prefix" />
                    <TextField source="title" label="Observation title" />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default GeneralRuleList;
