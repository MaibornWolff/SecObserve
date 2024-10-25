import { Fragment } from "react";
import {
    AutocompleteInput,
    Datagrid,
    FilterForm,
    ListContextProvider,
    ReferenceInput,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { PERMISSION_COMPONENT_LICENSE_DELETE } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { PURL_TYPE_CHOICES } from "../../core/types";
import { EVALUATION_RESULT_CHOICES } from "../types";
import LicenseComponentBulkDeleteButton from "./LicenseComponentBulkDeleteButton";

const showLicenseComponent = (id: any) => {
    return "../../../../license_components/" + id + "/show";
};

function listFilters(product: any) {
    const filters = [];
    filters.push(<TextInput source="license_spdx_id" label="SPDX Id" alwaysOn />);
    filters.push(<TextInput source="unknown_license" alwaysOn />);
    filters.push(
        <AutocompleteInputMedium
            source="evaluation_result"
            label="Evaluation result"
            choices={EVALUATION_RESULT_CHOICES}
            alwaysOn
        />
    );
    if (product && product.has_branches) {
        filters.push(
            <ReferenceInput
                source="branch"
                reference="branches"
                sort={{ field: "name", order: "ASC" }}
                filter={{ product: product.id }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" label="Branch / Version" />
            </ReferenceInput>
        );
    }
    filters.push(<TextInput source="name_version" label="Component" alwaysOn />);
    filters.push(<AutocompleteInput source="purl_type" label="Component type" choices={PURL_TYPE_CHOICES} alwaysOn />);

    return filters;
}

type LicenseComponentEmbeddedListProps = {
    product: any;
};

const BulkActionButtons = (product: any) => (
    <Fragment>
        {product.product.permissions.includes(PERMISSION_COMPONENT_LICENSE_DELETE) && (
            <LicenseComponentBulkDeleteButton product={product.product} />
        )}
    </Fragment>
);

const LicenseComponentEmbeddedList = ({ product }: LicenseComponentEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "license_components",
        sort: { field: "evaluation_result", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "license_components.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters(product)} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={showLicenseComponent}
                    bulkActionButtons={
                        product &&
                        product.permissions.includes(PERMISSION_COMPONENT_LICENSE_DELETE) && (
                            <BulkActionButtons product={product} />
                        )
                    }
                    resource="license_components"
                >
                    <TextField source="license_data.spdx_id" label="SPDX Id" />
                    <TextField source="unknown_license" label="Unknown license" />
                    <EvaluationResultField source="evaluation_result" label="Evaluation result" />
                    {product && product.has_branches && <TextField source="branch_name" label="Branch / Version" />}
                    <TextField source="name_version" label="Component" />
                    <TextField source="purl_type" label="Component type" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default LicenseComponentEmbeddedList;
