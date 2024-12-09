import {
    AutocompleteInput,
    Datagrid,
    DateField,
    FilterForm,
    FunctionField,
    ListContextProvider,
    ReferenceInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { feature_vex_enabled } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { ASSESSMENT_STATUS_NEEDS_APPROVAL } from "../types";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";
import { commentShortened } from "./functions";

function listFilters(product: any) {
    const filters = [];
    if (product && product.has_branches) {
        filters.push(
            <ReferenceInput
                source="branch"
                reference="branches"
                queryOptions={{ meta: { api_resource: "branch_names" } }}
                sort={{ field: "name", order: "ASC" }}
                filter={{ product: product.id }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" label="Branch / Version" />
            </ReferenceInput>
        );
    }
    filters.push(<TextInput source="observation_title" label="Observation title" alwaysOn />);

    if (product && product.has_component) {
        filters.push(<TextInput source="origin_component_name_version" label="Component" alwaysOn />);
    }
    if (product && product.has_docker_image) {
        filters.push(<TextInput source="origin_docker_image_name_tag_short" label="Container" alwaysOn />);
    }
    if (product && product.has_endpoint) {
        filters.push(<TextInput source="origin_endpoint_hostname" label="Host" alwaysOn />);
    }
    if (product && product.has_source) {
        filters.push(<TextInput source="origin_source_file" label="Source" alwaysOn />);
    }
    if (product && product.has_cloud_resource) {
        filters.push(<TextInput source="origin_cloud_qualified_resource" label="Cloud resource" alwaysOn />);
    }
    if (product && product.has_kubernetes_resource) {
        filters.push(<TextInput source="origin_kubernetes_qualified_resource" label="Kubernetes resource" alwaysOn />);
    }

    filters.push(
        <ReferenceInput source="user" reference="users" sort={{ field: "full_name", order: "ASC" }} alwaysOn>
            <AutocompleteInputMedium optionText="full_name" />
        </ReferenceInput>,
        <AutocompleteInput source="severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
        <AutocompleteInput source="status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />
    );
    return filters;
}

type ObservationLogApprovalEmbeddedListProps = {
    product: any;
};

const ObservationLogApprovalEmbeddedList = ({ product }: ObservationLogApprovalEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id), assessment_status: ASSESSMENT_STATUS_NEEDS_APPROVAL },
        perPage: 25,
        resource: "observation_logs",
        sort: { field: "created", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "observation_logs.approvalembedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    const ShowObservationLogs = (id: any) => {
        return "../../../../observation_logs/" + id + "/show";
    };

    localStorage.setItem("observationlogapprovalembeddedlist", "true");
    localStorage.removeItem("observationlogapprovallist");
    localStorage.removeItem("observationlogembeddedlist");

    return (
        <ResourceContextProvider value="observation_logs">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <FilterForm filters={listFilters(product)} />
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                        rowClick={ShowObservationLogs}
                        resource="observation_logs"
                    >
                        {product && product.has_branches && <TextField source="branch_name" label="Branch / Version" />}
                        <TextField source="observation_data.title" label="Observation" />
                        {product && product.has_component && (
                            <TextField
                                source="observation_data.origin_component_name_version"
                                label="Component"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {product && product.has_docker_image && (
                            <TextField
                                source="observation_data.origin_docker_image_name_tag_short"
                                label="Container"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {product && product.has_endpoint && (
                            <TextField
                                source="observation_data.origin_endpoint_hostname"
                                label="Host"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {product && product.has_source && (
                            <TextField
                                source="observation_data.origin_source_file"
                                label="Source"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {product && product.has_cloud_resource && (
                            <TextField
                                source="observation_data.origin_cloud_qualified_resource"
                                label="Cloud resource"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {product && product.has_kubernetes_resource && (
                            <TextField
                                source="observation_data.origin_kubernetes_qualified_resource"
                                label="Kubernetes resource"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
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
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default ObservationLogApprovalEmbeddedList;
