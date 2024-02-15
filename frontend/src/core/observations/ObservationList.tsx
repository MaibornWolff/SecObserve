import { Stack } from "@mui/material";
import {
    AutocompleteInput,
    BooleanField,
    ChipField,
    Datagrid,
    FilterButton,
    FunctionField,
    List,
    NullableBooleanInput,
    NumberField,
    ReferenceInput,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/settings/functions";
import {
    AGE_CHOICES,
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
        <AutocompleteInputWide optionText="name_with_product" />
    </ReferenceInput>,
    <TextInput source="title" alwaysOn />,
    <AutocompleteInput source="current_severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
    <AutocompleteInput source="current_status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
    <ReferenceInput label="Service" source="origin_service" reference="services" sort={{ field: "name", order: "ASC" }}>
        <AutocompleteInputWide label="Service" optionText="name_with_product" />
    </ReferenceInput>,
    <TextInput source="origin_component_name_version" label="Component" />,
    <TextInput source="origin_docker_image_name_tag_short" label="Container" />,
    <TextInput source="origin_endpoint_hostname" label="Host" />,
    <TextInput source="origin_source_file" label="Source" />,
    <TextInput source="origin_cloud_qualified_resource" label="Resource" />,
    <TextInput source="vulnerability_id" label="Vulnerability ID" alwaysOn />,
    <TextInput source="scanner" alwaysOn />,
    <AutocompleteInputMedium source="age" choices={AGE_CHOICES} alwaysOn />,
    <NullableBooleanInput source="has_potential_duplicates" label="Duplicates" alwaysOn />,
];

const ListActions = () => (
    <TopToolbar>
        <Stack spacing={0.5} alignItems="flex-end">
            <FilterButton />
        </Stack>
    </TopToolbar>
);

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
            actions={<ListActions />}
        >
            <Datagrid size={getSettingListSize()} rowClick="show" bulkActionButtons={false}>
                <TextField source="product_data.name" label="Product" />
                <TextField source="product_data.product_group_name" label="Group" />
                <TextField source="branch_name" label="Branch" />
                <TextField source="title" />
                <SeverityField source="current_severity" />
                <ChipField source="current_status" label="Status" />
                <NumberField source="epss_score" label="EPSS" />
                <TextField source="origin_service_name" label="Service" />
                <TextField source="origin_component_name_version" label="Component" />
                <TextField source="origin_docker_image_name_tag_short" label="Container" />
                <TextField source="origin_endpoint_hostname" label="Host" />
                <TextField source="origin_source_file" label="Source" />
                <TextField source="origin_cloud_qualified_resource" label="Resource" />,
                <TextField source="scanner_name" label="Scanner" />
                <FunctionField<Observation>
                    label="Age"
                    sortBy="last_observation_log"
                    render={(record) => (record ? humanReadableDate(record.last_observation_log) : "")}
                />
                <BooleanField source="has_potential_duplicates" label="Dupl." />
            </Datagrid>
        </List>
    );
};

export default ObservationList;
