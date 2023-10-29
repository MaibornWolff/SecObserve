import { Paper, Stack } from "@mui/material";
import { Fragment } from "react";
import {
    AutocompleteInput,
    ChipField,
    DatagridConfigurable,
    FilterForm,
    FunctionField,
    ListContextProvider,
    NumberField,
    Pagination,
    ReferenceInput,
    SelectColumnsButton,
    TextField,
    TextInput,
    TopToolbar,
    useListController,
} from "react-admin";

import { PERMISSION_OBSERVATION_ASSESSMENT, PERMISSION_OBSERVATION_DELETE } from "../../access_control/types";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import {
    OBSERVATION_AGE_CHOICES,
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
    Observation,
    Product,
} from "../types";
import ObservationBulkAssessment from "./ObservationBulkAssessment";
import ObservationBulkDeleteButton from "./ObservationBulkDeleteButton";

function listFilters(product: Product) {
    return [
        <ReferenceInput
            source="branch"
            reference="branches"
            sort={{ field: "name", order: "ASC" }}
            filter={{ product: product.id }}
            alwaysOn
        >
            <AutocompleteInputMedium optionText="name" />
        </ReferenceInput>,
        <TextInput source="title" alwaysOn />,
        <AutocompleteInput
            source="current_severity"
            label="Severity"
            choices={OBSERVATION_SEVERITY_CHOICES}
            alwaysOn
        />,
        <AutocompleteInput source="current_status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
        <TextInput source="origin_service_name" label="Service" alwaysOn />,
        <TextInput source="origin_component_name_version" label="Component" alwaysOn />,
        <TextInput source="origin_docker_image_name_tag_short" label="Container" alwaysOn />,
        <TextInput source="origin_endpoint_hostname" label="Host" alwaysOn />,
        <TextInput source="origin_source_file" label="Source" alwaysOn />,
        <TextInput source="scanner" alwaysOn />,
        <AutocompleteInputMedium source="age" choices={OBSERVATION_AGE_CHOICES} alwaysOn />,
        <TextInput source="upload_filename" label="Filename" />,
        <TextInput source="api_configuration_name" label="API configuration" />,
    ];
}

const ShowObservations = (id: any) => {
    return "../../../../observations/" + id + "/show";
};

type ObservationsEmbeddedListProps = {
    product: any;
};

const BulkActionButtons = (product: any) => (
    <Fragment>
        {product.product.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT) && (
            <ObservationBulkAssessment product={product.product} />
        )}
        {product.product.permissions.includes(PERMISSION_OBSERVATION_DELETE) && (
            <ObservationBulkDeleteButton product={product.product} />
        )}
    </Fragment>
);

const ListActions = () => (
    <TopToolbar>
        <SelectColumnsButton preferenceKey="observations.embedded" />
    </TopToolbar>
);

const ObservationsEmbeddedList = ({ product }: ObservationsEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "observations",
        sort: { field: "current_severity", order: "ASC" },
        filterDefaultValues: { current_status: OBSERVATION_STATUS_OPEN, branch: product.repository_default_branch },
        disableSyncWithLocation: false,
        storeKey: "observations.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    localStorage.setItem("observationembeddedlist.product", product.id);

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Stack direction="row" spacing={2} justifyContent="center" alignItems="flex-end">
                    <FilterForm filters={listFilters(product)} />
                    <ListActions />
                </Stack>
                <Paper>
                    <DatagridConfigurable
                        size="medium"
                        sx={{ width: "100%" }}
                        rowClick={ShowObservations}
                        bulkActionButtons={
                            product &&
                            (product.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT) ||
                                product.permissions.includes(PERMISSION_OBSERVATION_DELETE)) && (
                                <BulkActionButtons product={product} />
                            )
                        }
                        preferenceKey="observations.embedded"
                    >
                        <TextField source="branch_name" label="Branch" />
                        <TextField source="title" />
                        <SeverityField source="current_severity" />
                        <NumberField source="epss_score" label="EPSS" />
                        <ChipField source="current_status" label="Status" />
                        <TextField source="origin_service_name" label="Service" />
                        <TextField source="origin_component_name_version" label="Component" />
                        <TextField source="origin_docker_image_name_tag_short" label="Container" />
                        <TextField source="origin_endpoint_hostname" label="Host" />
                        <TextField source="origin_source_file" label="Source" />
                        <TextField source="scanner_name" label="Scanner" />
                        <FunctionField<Observation>
                            label="Age"
                            sortBy="last_observation_log"
                            render={(record) => (record ? humanReadableDate(record.last_observation_log) : "")}
                        />
                    </DatagridConfigurable>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ObservationsEmbeddedList;
