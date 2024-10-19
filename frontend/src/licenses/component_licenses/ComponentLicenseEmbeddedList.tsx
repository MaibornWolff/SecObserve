import {
    Datagrid,
    FilterForm,
    ListContextProvider,
    NumberField,
    ReferenceInput,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { EVALUATION_RESULT_CHOICES } from "../types";

const showComponentLicense = (id: any) => {
    return "../../../../component_licenses/" + id + "/show";
};

function listFilters(product: any) {
    const filters = [];
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
    filters.push(<TextInput source="license_spdx_id" label="SPDX Id" alwaysOn />);
    filters.push(<TextInput source="unkown_license" alwaysOn />);
    filters.push(
        <AutocompleteInputMedium
            source="evaluation_result"
            label="Evaluation result"
            choices={EVALUATION_RESULT_CHOICES}
            alwaysOn
        />
    );

    return filters;
}

type ComponentLicenseEmbeddedListProps = {
    product: any;
};

const ComponentLicenseEmbeddedList = ({ product }: ComponentLicenseEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "component_licenses",
        sort: { field: "license_spdx_id", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "component_licenses.embedded",
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
                    rowClick={showComponentLicense}
                    bulkActionButtons={false}
                    resource="component_licenses"
                >
                    {product && product.has_branches && (
                        <TextField source="vulnerability_check_data.branch_name" label="Branch / Version" />
                    )}
                    <TextField source="license_spdx_id" label="License" />
                    <TextField source="unknown_license" label="Unknown license" />
                    <EvaluationResultField source="evaluation_result" label="Evaluation result" />
                    <NumberField source="num_components" label="# Components" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ComponentLicenseEmbeddedList;
