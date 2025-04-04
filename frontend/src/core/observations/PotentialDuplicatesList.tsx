import { Fragment } from "react";
import {
    ChipField,
    Datagrid,
    FunctionField,
    ListContextProvider,
    ResourceContextProvider,
    TextField,
    useListController,
} from "react-admin";

import { PERMISSION_OBSERVATION_ASSESSMENT } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { OBSERVATION_STATUS_OPEN, Observation } from "../types";
import ObservationBulkDuplicatesButton from "./ObservationBulkDuplicatesButton";

const ShowObservations = (id: any, resource: any, record: any) => {
    return "../../../../observations/" + record.potential_duplicate_observation.id + "/show";
};

type PotentialDuplicatesListProps = {
    observation: any;
};

const BulkActionButtons = (observation: any) => (
    <Fragment>
        {observation?.observation?.product_data?.permissions?.includes(PERMISSION_OBSERVATION_ASSESSMENT) && (
            <ObservationBulkDuplicatesButton observation={observation.observation} />
        )}
    </Fragment>
);

const PotentialDuplicatesList = ({ observation }: PotentialDuplicatesListProps) => {
    const listContext = useListController({
        filter: { observation: Number(observation.id), status: OBSERVATION_STATUS_OPEN },
        perPage: 25,
        resource: "potential_duplicates",
        sort: { field: "potential_duplicate_observation.current_severity", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: "potential_duplicates",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="potential_duplicates">
            <ListContextProvider value={listContext}>
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={ShowObservations}
                    bulkActionButtons={<BulkActionButtons observation={observation} />}
                    resource="potential_duplicates"
                >
                    <TextField source="potential_duplicate_observation.title" label="Title" />
                    <SeverityField label="Severity" source="potential_duplicate_observation.current_severity" />
                    <ChipField source="potential_duplicate_observation.current_status" label="Status" />
                    <TextField source="potential_duplicate_observation.origin_service_name" label="Service" />
                    {observation?.product_data?.has_component && (
                        <TextField
                            source="potential_duplicate_observation.origin_component_name_version"
                            label="Component"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    {observation?.product_data?.has_docker_image && (
                        <TextField
                            source="potential_duplicate_observation.origin_docker_image_name_tag_short"
                            label="Container"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    {observation?.product_data?.has_endpoint && (
                        <TextField
                            source="potential_duplicate_observation.origin_endpoint_hostname"
                            label="Host"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    {observation?.product_data?.has_source && (
                        <TextField
                            source="potential_duplicate_observation.origin_source_file"
                            label="Source"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    {observation?.product_data?.has_cloud_resource && (
                        <TextField
                            source="potential_duplicate_observation.origin_cloud_qualified_resource"
                            label="Cloud resource"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    {observation?.product_data?.has_kubernetes_resource && (
                        <TextField
                            source="potential_duplicate_observation.origin_kubernetes_qualified_resource"
                            label="Kubernetes resource"
                            sx={{ wordBreak: "break-word" }}
                        />
                    )}
                    <TextField source="potential_duplicate_observation.scanner_name" label="Scanner" />
                    <FunctionField<Observation>
                        label="Age"
                        sortBy="potential_duplicate_observation.last_observation_log"
                        render={(record) =>
                            record ? humanReadableDate(record.potential_duplicate_observation.last_observation_log) : ""
                        }
                    />
                </Datagrid>
                <CustomPagination />
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default PotentialDuplicatesList;
