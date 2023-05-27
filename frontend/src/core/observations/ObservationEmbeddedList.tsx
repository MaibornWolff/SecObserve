import { Paper } from "@mui/material";
import { Fragment } from "react";
import {
    AutocompleteInput,
    ChipField,
    Datagrid,
    FilterForm,
    FunctionField,
    ListContextProvider,
    Pagination,
    TextField,
    TextInput,
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
} from "../types";
import ObservationBulkAssessment from "./ObservationBulkAssessment";
import ObservationBulkDeleteButton from "./ObservationBulkDeleteButton";

const listFilters = [
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

const ObservationsEmbeddedList = ({ product }: ObservationsEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "observations";
    const sort = { field: "current_severity", order: "ASC" };
    const filterDefaultValues = { current_status: OBSERVATION_STATUS_OPEN };
    const disableSyncWithLocation = false;
    const storeKey = "observations.embedded";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        filterDefaultValues,
        disableSyncWithLocation,
        storeKey,
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
                <FilterForm filters={listFilters} />
                <Paper>
                    <Datagrid
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
                    >
                        <TextField source="title" />
                        <SeverityField source="current_severity" />
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
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ObservationsEmbeddedList;
