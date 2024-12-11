import { Fragment } from "react";
import {
    AutocompleteInput,
    BooleanField,
    ChipField,
    Datagrid,
    FilterForm,
    FunctionField,
    ListContextProvider,
    NullableBooleanInput,
    NumberField,
    ReferenceInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { PERMISSION_OBSERVATION_ASSESSMENT } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import {
    AGE_CHOICES,
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_IN_REVIEW,
    Observation,
    PURL_TYPE_CHOICES,
    Product,
} from "../types";
import ObservationBulkAssessment from "./ObservationBulkAssessment";
import ObservationExpand from "./ObservationExpand";
import {
    IDENTIFIER_OBSERVATION_REVIEW_LIST,
    IDENTIFIER_OBSERVATION_REVIEW_LIST_PRODUCT,
    setListIdentifier,
} from "./functions";

function listFilters(product: Product) {
    const filters = [];
    if (!product) {
        filters.push(
            <ReferenceInput
                source="product"
                reference="products"
                sort={{ field: "name", order: "ASC" }}
                queryOptions={{ meta: { api_resource: "product_names" } }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" />
            </ReferenceInput>
        );
    }
    if (!product) {
        filters.push(
            <ReferenceInput
                source="product_group"
                reference="product_groups"
                sort={{ field: "name", order: "ASC" }}
                queryOptions={{ meta: { api_resource: "product_group_names" } }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" />
            </ReferenceInput>
        );
    }
    if (!product) {
        filters.push(
            <ReferenceInput
                source="branch"
                reference="branches"
                sort={{ field: "name", order: "ASC" }}
                queryOptions={{ meta: { api_resource: "branch_names" } }}
                alwaysOn
            >
                <AutocompleteInputWide optionText="name_with_product" label="Branch / Version" />
            </ReferenceInput>
        );
    }
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
    filters.push(<TextInput source="title" alwaysOn />);
    filters.push(
        <AutocompleteInput source="current_severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />
    );
    if (product && product.has_services) {
        filters.push(
            <ReferenceInput
                source="origin_service"
                reference="services"
                sort={{ field: "name", order: "ASC" }}
                filter={{ product: product.id }}
                alwaysOn
            >
                <AutocompleteInputMedium label="Service" optionText="name" />
            </ReferenceInput>
        );
    }

    if (!product || (product && product.has_component)) {
        filters.push(<TextInput source="origin_component_name_version" label="Component" alwaysOn />);
        filters.push(
            <AutocompleteInput
                source="origin_component_purl_type"
                label="Component type"
                choices={PURL_TYPE_CHOICES}
                alwaysOn
            />
        );
    }
    if (!product || (product && product.has_docker_image)) {
        filters.push(<TextInput source="origin_docker_image_name_tag_short" label="Container" alwaysOn />);
    }
    if (!product || (product && product.has_endpoint)) {
        filters.push(<TextInput source="origin_endpoint_hostname" label="Host" alwaysOn />);
    }
    if (!product || (product && product.has_source)) {
        filters.push(<TextInput source="origin_source_file" label="Source" alwaysOn />);
    }
    if (!product || (product && product.has_cloud_resource)) {
        filters.push(<TextInput source="origin_cloud_qualified_resource" label="Cloud resource" alwaysOn />);
    }
    if (!product || (product && product.has_kubernetes_resource)) {
        filters.push(<TextInput source="origin_kubernetes_qualified_resource" label="Kubernetes resource" alwaysOn />);
    }

    filters.push(<TextInput source="scanner" alwaysOn />);
    filters.push(<AutocompleteInputMedium source="age" choices={AGE_CHOICES} alwaysOn />);
    if (product && product.has_potential_duplicates) {
        filters.push(<NullableBooleanInput source="has_potential_duplicates" label="Duplicates" alwaysOn />);
    }

    return filters;
}

const ShowObservations = (id: any) => {
    return "../../../../observations/" + id + "/show";
};

type ObservationsReviewListProps = {
    product?: any;
};

const BulkActionButtons = ({ product }: any) => (
    <Fragment>
        {(!product || (product && product.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT))) && (
            <ObservationBulkAssessment product={product} />
        )}
    </Fragment>
);

const ObservationsReviewList = ({ product }: ObservationsReviewListProps) => {
    if (product) {
        setListIdentifier(IDENTIFIER_OBSERVATION_REVIEW_LIST_PRODUCT);
    } else {
        setListIdentifier(IDENTIFIER_OBSERVATION_REVIEW_LIST);
    }

    let filter = {};
    filter = { current_status: OBSERVATION_STATUS_IN_REVIEW };
    let filterDefaultValues = {};
    let storeKey = "observations.review";
    if (product) {
        filter = { ...filter, product: Number(product.id) };
        filterDefaultValues = { branch: product.repository_default_branch };
        storeKey = "observations.review.product";
    }

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: "observations",
        sort: { field: "current_severity", order: "ASC" },
        filterDefaultValues: filterDefaultValues,
        disableSyncWithLocation: false,
        storeKey: storeKey,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="observations">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <FilterForm filters={listFilters(product)} />
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        rowClick={ShowObservations}
                        bulkActionButtons={
                            (!product ||
                                (product && product.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT))) && (
                                <BulkActionButtons product={product} />
                            )
                        }
                        resource="observations"
                        expand={<ObservationExpand />}
                        expandSingle
                    >
                        {!product && <TextField source="product_data.name" label="Product" />}
                        {!product && <TextField source="product_data.product_group_name" label="Group" />}
                        {(!product || (product && product.has_branches)) && (
                            <TextField source="branch_name" label="Branch / Version" />
                        )}
                        <TextField source="title" />
                        <SeverityField label="Severity" source="current_severity" />
                        {(!product || (product && product.has_component)) && (
                            <NumberField source="epss_score" label="EPSS" />
                        )}
                        <ChipField source="current_status" label="Status" />
                        {(!product || (product && product.has_services)) && (
                            <TextField source="origin_service_name" label="Service" />
                        )}
                        {(!product || (product && product.has_component)) && (
                            <TextField
                                source="origin_component_name_version"
                                label="Component"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {(!product || (product && product.has_docker_image)) && (
                            <TextField
                                source="origin_docker_image_name_tag_short"
                                label="Container"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {(!product || (product && product.has_endpoint)) && (
                            <TextField
                                source="origin_endpoint_hostname"
                                label="Host"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {(!product || (product && product.has_source)) && (
                            <TextField source="origin_source_file" label="Source" sx={{ wordBreak: "break-word" }} />
                        )}
                        {(!product || (product && product.has_cloud_resource)) && (
                            <TextField
                                source="origin_cloud_qualified_resource"
                                label="Cloud resource"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        {(!product || (product && product.has_kubernetes_resource)) && (
                            <TextField
                                source="origin_kubernetes_qualified_resource"
                                label="Kubernetes resource"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        <TextField source="scanner_name" label="Scanner" />
                        <FunctionField<Observation>
                            label="Age"
                            sortBy="last_observation_log"
                            render={(record) => (record ? humanReadableDate(record.last_observation_log) : "")}
                        />
                        {product && product.has_potential_duplicates && (
                            <BooleanField source="has_potential_duplicates" label="Dupl." />
                        )}
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default ObservationsReviewList;
