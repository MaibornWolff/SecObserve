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
import LicenseGroupCreateButton from "./LicenseGroupCreateButton";

const showLicenseGroup = (id: any) => {
    return "../../../../license_groups/" + id + "/show";
};

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <NullableBooleanInput source="is_public" label="Public" alwaysOn />,
];

type LicenseGroupEmbeddedListProps = {
    license: any;
};

const LicenseGroupEmbeddedList = ({ license }: LicenseGroupEmbeddedListProps) => {
    const filter = license ? { licenses: Number(license.id) } : {};
    const storeKey = license ? false : "licensegroups.embedded";

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: "license_groups",
        sort: { field: "name", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: storeKey,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="license_groups">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    {!is_external() && !license && <LicenseGroupCreateButton />}
                    {!license && <FilterForm filters={listFilters} />}
                    <Datagrid
                        size={getSettingListSize()}
                        rowClick={showLicenseGroup}
                        bulkActionButtons={false}
                        resource="license_groups"
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

export default LicenseGroupEmbeddedList;
