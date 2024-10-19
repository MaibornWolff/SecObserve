import { Stack } from "@mui/material";
import {
    Datagrid,
    FilterForm,
    ListContextProvider,
    TextField,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { is_superuser } from "../../commons/functions";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { EVALUATION_RESULT_CHOICES } from "../types";
import LicensePolicyItemAdd from "./LicensePolicyItemAdd";
import LicensePolicyItemEdit from "./LicensePolicyItemEdit";
import LicensePolicyItemRemove from "./LicensePolicyItemRemove";

function listFilters() {
    return [
        <TextInput source="license_group_name" label="License group" alwaysOn />,
        <TextInput source="license_spdx_id" label="License" alwaysOn />,
        <TextInput source="unknown_license" label="Unknown license" alwaysOn />,
        <AutocompleteInputMedium
            source="evaluation_result"
            label="Evaluation result"
            choices={EVALUATION_RESULT_CHOICES}
            alwaysOn
        />,
    ];
}

type LicensePolicyItemEmbeddedListProps = {
    license_policy: any;
};

const LicensePolicyItemEmbeddedList = ({ license_policy }: LicensePolicyItemEmbeddedListProps) => {
    const listContext = useListController({
        filter: { license_policy: Number(license_policy.id) },
        perPage: 25,
        resource: "license_policy_items",
        sort: { field: "evaluation_result", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: true,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                {(is_superuser() || license_policy.is_manager) && <LicensePolicyItemAdd id={license_policy.id} />}
                <FilterForm filters={listFilters()} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={false}
                    bulkActionButtons={false}
                    resource="license_policy_item"
                >
                    <TextField source="license_group_name" label="License group" />
                    <TextField source="license_spdx_id" label="License" />
                    <TextField source="unknown_license" label="Unknown license" />
                    <TextField source="evaluation_result" label="Evaluation result" />
                    {(is_superuser() || license_policy.is_manager) && (
                        <WithRecord
                            render={(license_policy_item) => (
                                <Stack direction="row" spacing={4}>
                                    <LicensePolicyItemEdit />
                                    <LicensePolicyItemRemove license_policy_item={license_policy_item} />
                                </Stack>
                            )}
                        />
                    )}
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default LicensePolicyItemEmbeddedList;
