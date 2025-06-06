import { Fragment, useEffect, useState } from "react";
import {
    Datagrid,
    FilterForm,
    FunctionField,
    ListContextProvider,
    ReferenceInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    WithListContext,
    useListController,
    useRecordContext,
} from "react-admin";

import { PERMISSION_COMPONENT_LICENSE_DELETE } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { EVALUATION_RESULT_CHOICES } from "../types";
import LicenseComponentBulkDeleteButton from "./LicenseComponentBulkDeleteButton";

type LicenseComponentEmbeddedListProps = {
    product: any;
    expand?: boolean;
    component_purl_type?: string;
    origin_service?: number;
};

const BulkActionButtons = (product: any) => (
    <Fragment>
        {product.product.permissions.includes(PERMISSION_COMPONENT_LICENSE_DELETE) && (
            <LicenseComponentBulkDeleteButton product={product.product} />
        )}
    </Fragment>
);

const licenseNameStyle = (type: string): string => {
    if (type === "" || type === "Non-SPDX" || type === "Multiple") {
        return "italic";
    }
    return "normal";
};

const LicenseComponentEmbeddedList = ({
    product,
    expand,
    component_purl_type,
    origin_service,
}: LicenseComponentEmbeddedListProps) => {
    const [initialExpand, setInitialExpand] = useState(true);

    const showLicenseComponent = (id: any) => {
        return "../../../../license_components/" + id + "/show";
    };

    function listFilters() {
        const filters = [];
        if (product?.has_branches) {
            filters.push(
                <ReferenceInput
                    source="branch"
                    reference="branches"
                    queryOptions={{ meta: { api_resource: "branch_names" } }}
                    sort={{ field: "name", order: "ASC" }}
                    filter={{ product: product.id, for_license_components: true }}
                    alwaysOn
                >
                    <AutocompleteInputMedium optionText="name" label="Branch / Version" />
                </ReferenceInput>
            );
        }
        filters.push(
            <TextInput source="license_name" label="License" alwaysOn />,
            <AutocompleteInputMedium
                source="evaluation_result"
                label="Evaluation result"
                choices={EVALUATION_RESULT_CHOICES}
                alwaysOn
            />,
            <TextInput source="component_name_version" label="Component" alwaysOn />,
            <ReferenceInput
                source="component_purl_type"
                reference="purl_types"
                filter={{ product: product.id, for_license_components: true }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" label="Component type" />
            </ReferenceInput>
        );
        if (product?.has_services) {
            filters.push(
                <ReferenceInput
                    source="origin_service"
                    reference="services"
                    queryOptions={{ meta: { api_resource: "service_names" } }}
                    sort={{ field: "name", order: "ASC" }}
                    filter={{ product: product.id }}
                    alwaysOn
                >
                    <AutocompleteInputMedium label="Service" optionText="name" />
                </ReferenceInput>
            );
        }

        return filters;
    }

    let filter: any = { product: Number(product.id) };
    let filterDefaultValues: any = {};

    const record = useRecordContext();
    if (expand) {
        if (initialExpand) {
            localStorage.removeItem("RaStore.license_components.embedded");
            setInitialExpand(false);
        }
        if (record?.branch_name) {
            filter = { ...filter, branch_name_exact: record.branch_name };
        }
        if (record?.license_name) {
            filter = { ...filter, license_name_exact: record.license_name };
        }
        if (record?.evaluation_result) {
            filter = { ...filter, evaluation_result: record.evaluation_result };
        }
        if (component_purl_type) {
            filter = { ...filter, component_purl_type: component_purl_type };
        }
        if (origin_service) {
            filter = { ...filter, origin_service: origin_service };
        }
        if (record) {
            const storedFilters = {
                branch_name: record.branch_name,
                license_name: record.license_name,
                evaluation_result: record.evaluation_result,
                component_purl_type: component_purl_type,
                origin_service: origin_service,
            };
            localStorage.setItem("license_component_expand_filters", JSON.stringify({ storedFilters }));
        }
    } else {
        filterDefaultValues = { branch: product.repository_default_branch };
        localStorage.removeItem("license_component_expand_filters");
    }

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: "license_components",
        sort: { field: "evaluation_result", order: "ASC" },
        filterDefaultValues: filterDefaultValues,
        disableSyncWithLocation: true,
        storeKey: "license_components.embedded",
    });

    useEffect(() => {
        const storage = localStorage.getItem("RaStore.license_components.embedded");
        if (storage) {
            localStorage.setItem("RaStore.license_components.overview", storage);
        }
    }, [listContext.filterValues, listContext.sort]);

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="license_components">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    {!expand && <FilterForm filters={listFilters()} />}
                    <Datagrid
                        size={getSettingListSize()}
                        rowClick={showLicenseComponent}
                        bulkActionButtons={
                            product?.permissions.includes(PERMISSION_COMPONENT_LICENSE_DELETE) && (
                                <BulkActionButtons product={product} />
                            )
                        }
                        resource="license_components"
                    >
                        {!expand && product?.has_branches && (
                            <TextField source="branch_name" label="Branch / Version" />
                        )}
                        <FunctionField
                            label="License"
                            sortBy="license_name"
                            render={(record: any) => (
                                <span style={{ fontStyle: licenseNameStyle(record.type) }}>{record.license_name}</span>
                            )}
                        />
                        {!expand && (
                            <EvaluationResultField
                                source="evaluation_result"
                                label="Evaluation result"
                                sortable={true}
                            />
                        )}
                        <TextField source="component_name_version_type" label="Component" />
                        {product?.has_services && <TextField source="origin_service_name" label="Service" />}
                    </Datagrid>
                    <WithListContext
                        render={({ total }) => (
                            <Fragment>{((expand && total && total > 25) || !expand) && <CustomPagination />}</Fragment>
                        )}
                    />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default LicenseComponentEmbeddedList;
