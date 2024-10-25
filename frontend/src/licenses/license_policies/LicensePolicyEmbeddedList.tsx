import {
    BooleanField,
    Datagrid,
    FilterForm,
    ListContextProvider,
    NullableBooleanInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { is_external } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import LicensePolicyCreateButton from "./LicensePolicyCreateButton";

const showLicensePolicy = (id: any) => {
    return "../../../../license_policies/" + id + "/show";
};

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <NullableBooleanInput source="is_public" label="Public" alwaysOn />,
];

type LicensePolicyEmbeddedListProps = {
    license: any;
};

const LicensePolicyEmbeddedList = ({ license }: LicensePolicyEmbeddedListProps) => {
    const filter = license ? { licenses: Number(license.id) } : {};
    const storeKey = license ? false : "license_policies.embedded";

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: "license_policies",
        sort: { field: "name", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: storeKey,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    localStorage.setItem("licensepolicyembeddedlist", "true");
    localStorage.removeItem("licenseotherlist");

    return (
        <ResourceContextProvider value="license_policies">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    {!is_external() && !license && <LicensePolicyCreateButton />}
                    <FilterForm filters={listFilters} />
                    <Datagrid
                        size={getSettingListSize()}
                        rowClick={showLicensePolicy}
                        bulkActionButtons={false}
                        resource="license_policies"
                    >
                        <TextField source="name" label="Name" />
                        <BooleanField source="is_public" label="Public" />
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default LicensePolicyEmbeddedList;
