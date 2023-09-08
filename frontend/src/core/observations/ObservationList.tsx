import {
    AutocompleteInput,
    ChipField,
    Datagrid,
    FunctionField,
    List,
    NumberField,
    ReferenceInput,
    TextField,
    TextInput,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import {
    OBSERVATION_AGE_CHOICES,
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
    Observation,
} from "../types";

const listFilters = [
    <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <ReferenceInput source="product_group" reference="product_groups" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <ReferenceInput source="branch" reference="branches" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <TextInput source="title" alwaysOn />,
    <AutocompleteInput source="current_severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
    <AutocompleteInput source="current_status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
    <TextInput source="origin_service_name" label="Service" alwaysOn />,
    <TextInput source="origin_component_name_version" label="Component" alwaysOn />,
    <TextInput source="origin_docker_image_name_tag_short" label="Container" alwaysOn />,
    <TextInput source="origin_endpoint_hostname" label="Host" alwaysOn />,
    <TextInput source="origin_source_file" label="Source" alwaysOn />,
    <TextInput source="scanner" alwaysOn />,
    <AutocompleteInputMedium source="age" choices={OBSERVATION_AGE_CHOICES} alwaysOn />,
];

const ObservationList = () => {
    localStorage.removeItem("observationembeddedlist.product");
    localStorage.removeItem("observationdashboardlist");

    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "current_severity", order: "ASC" }}
            filterDefaultValues={{ current_status: OBSERVATION_STATUS_OPEN }}
            disableSyncWithLocation={false}
            storeKey="observations.list"
            actions={false}
        >
            <Datagrid size="medium" rowClick="show" bulkActionButtons={false}>
                <TextField source="product_data.name" label="Product" />
                <TextField source="product_data.product_group_name" label="Group" />
                <TextField source="branch_name" label="Branch" />
                <TextField source="title" />
                <SeverityField source="current_severity" />
                <NumberField source="epss_score" label="EPSS" />
                <ChipField source="current_status" label="Status" />
                <TextField source="origin_service_name" label="Service" />
                <TextField source="origin_component_name_version" label="Component" />
                <TextField source="origin_docker_image_name_tag_short" label="Container" />
                <TextField source="origin_endpoint_hostname" label="Host" />
                <TextField source="origin_source_file" label="Source" />,
                <TextField source="scanner_name" label="Scanner" />
                <FunctionField<Observation>
                    label="Age"
                    sortBy="last_observation_log"
                    render={(record) => (record ? humanReadableDate(record.last_observation_log) : "")}
                />
            </Datagrid>
        </List>
    );
};

export default ObservationList;
