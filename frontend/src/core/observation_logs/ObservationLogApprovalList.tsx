import ChecklistIcon from "@mui/icons-material/Checklist";
import {
    AutocompleteInput,
    Datagrid,
    DateField,
    FunctionField,
    List,
    ReferenceInput,
    TextField,
    TextInput,
} from "react-admin";
import { Fragment } from "react/jsx-runtime";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { feature_vex_enabled } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium, AutocompleteInputWide } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { ASSESSMENT_STATUS_NEEDS_APPROVAL } from "../types";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";
import AssessmentBulkApproval from "./AssessmentBulkApproval";
import { commentShortened } from "./functions";

const BulkActionButtons = () => (
    <Fragment>
        <AssessmentBulkApproval />
    </Fragment>
);

const listFilters = [
    <ReferenceInput
        source="product"
        reference="products"
        sort={{ field: "name", order: "ASC" }}
        queryOptions={{ meta: { api_resource: "product_names" } }}
        alwaysOn
    >
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <ReferenceInput
        source="product_group"
        reference="product_groups"
        sort={{ field: "name", order: "ASC" }}
        queryOptions={{ meta: { api_resource: "product_group_names" } }}
        alwaysOn
    >
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <ReferenceInput
        source="branch"
        reference="branches"
        sort={{ field: "name", order: "ASC" }}
        queryOptions={{ meta: { api_resource: "branch_names" } }}
        alwaysOn
    >
        <AutocompleteInputWide optionText="name_with_product" label="Branch / Version" />
    </ReferenceInput>,
    <TextInput source="observation_title" label="Observation title" alwaysOn />,
    <ReferenceInput source="user" reference="users" sort={{ field: "full_name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="full_name" />
    </ReferenceInput>,
    <AutocompleteInput source="severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
    <AutocompleteInput source="status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
    <TextInput source="origin_component_name_version" label="Component" alwaysOn />,
];

const ObservationLogApprovalList = () => {
    localStorage.setItem("observationlogapprovallist", "true");
    localStorage.removeItem("observationlogapprovalembeddedlist");
    localStorage.removeItem("observationlogembeddedlist");

    return (
        <Fragment>
            <ListHeader icon={ChecklistIcon} title="Observation Log Reviews" />
            <List
                filter={{ assessment_status: ASSESSMENT_STATUS_NEEDS_APPROVAL }}
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "created", order: "ASC" }}
                disableSyncWithLocation={false}
                storeKey="observation_logs.approval"
                actions={false}
                sx={{ marginTop: 1 }}
            >
                <Datagrid size={getSettingListSize()} rowClick="show" bulkActionButtons={<BulkActionButtons />}>
                    <TextField source="observation_data.product_data.name" label="Product" />
                    <TextField source="observation_data.product_data.product_group_name" label="Group" />
                    <TextField source="branch_name" label="Branch / Version" />
                    <TextField source="observation_data.title" label="Observation" />
                    <TextField source="user_full_name" label="User" />
                    <TextField source="severity" emptyText="---" />
                    <TextField source="status" emptyText="---" />
                    {feature_vex_enabled() && (
                        <TextField
                            label="VEX justification"
                            source="vex_justification"
                            emptyText="---"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    <FunctionField
                        label="Comment"
                        render={(record) => commentShortened(record.comment)}
                        sortable={false}
                        sx={{ wordBreak: "break-word" }}
                    />
                    <DateField source="created" showTime />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default ObservationLogApprovalList;
