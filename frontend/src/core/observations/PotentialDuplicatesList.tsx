import { Fragment } from "react";
import { ChipField, Datagrid, FunctionField, ListContextProvider, TextField, useListController } from "react-admin";

import { PERMISSION_OBSERVATION_ASSESSMENT } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { getSettingListSize } from "../../commons/settings/functions";
import { OBSERVATION_STATUS_OPEN } from "../types";
import { Observation } from "../types";
import ObservationBulkDuplicatesButton from "./ObservationBulkDuplicatesButton";

const ShowObservations = (id: any, resource: any, record: any) => {
    return "../../../../observations/" + record.potential_duplicate_observation.id + "/show";
};

type PotentialDuplicatesListProps = {
    observation: any;
};

const BulkActionButtons = (observation: any) => (
    <Fragment>
        {observation &&
            observation.observation &&
            observation.observation.product_data &&
            observation.observation.product_data.permissions &&
            observation.observation.product_data.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT) && (
                <ObservationBulkDuplicatesButton observation={observation.observation} />
            )}
    </Fragment>
);

const PotentialDuplicatesList = ({ observation }: PotentialDuplicatesListProps) => {
    const listContext = useListController({
        filter: { observation: Number(observation.id), status: OBSERVATION_STATUS_OPEN },
        perPage: 25,
        resource: "potential_duplicates",
        sort: { field: "current_severity", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: "potential_duplicates",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    return (
        <ListContextProvider value={listContext}>
            <Datagrid
                size={getSettingListSize()}
                rowClick={ShowObservations}
                bulkActionButtons={<BulkActionButtons observation={observation} />}
            >
                <TextField source="potential_duplicate_observation.title" label="Title" />
                <SeverityField source="potential_duplicate_observation.current_severity" />
                <ChipField source="potential_duplicate_observation.current_status" label="Status" />
                <TextField source="potential_duplicate_observation.origin_service_name" label="Service" />
                <TextField source="potential_duplicate_observation.origin_component_name_version" label="Component" />
                <TextField
                    source="potential_duplicate_observation.origin_docker_image_name_tag_short"
                    label="Container"
                />
                <TextField source="potential_duplicate_observation.origin_endpoint_hostname" label="Host" />
                <TextField source="potential_duplicate_observation.origin_source_file" label="Source" />
                <TextField source="potential_duplicate_observation.origin_cloud_qualified_resource" label="Resource" />
                ,
                <TextField source="potential_duplicate_observation.scanner_name" label="Scanner" />
                <FunctionField<Observation>
                    label="Age"
                    sortBy="last_observation_log"
                    render={(record) =>
                        record ? humanReadableDate(record.potential_duplicate_observation.last_observation_log) : ""
                    }
                />
            </Datagrid>
            <CustomPagination />
        </ListContextProvider>
    );
};

export default PotentialDuplicatesList;
