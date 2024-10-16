import {
    BooleanField,
    Datagrid,
    FilterForm,
    ListContextProvider,
    NullableBooleanInput,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";

const showLicense = (id: any) => {
    return "../../../../licenses/" + id + "/show";
};

function listFilters(license_group: any) {
    const list_filters = [
        <TextInput source="license_id" alwaysOn />,
        <TextInput source="name" alwaysOn />,
        <NullableBooleanInput source="is_osi_approved" label="OSI approved" alwaysOn />,
        <NullableBooleanInput source="is_deprecated" label="Deprecated" alwaysOn />,
    ];
    if (license_group === null) {
        list_filters.push(<NullableBooleanInput source="is_in_license_group" label="In license group" alwaysOn />);
    }
    return list_filters;
}

type LicenseEmbeddedListProps = {
    license_group: any;
};

const LicenseEmbeddedList = ({ license_group }: LicenseEmbeddedListProps) => {
    const filter = license_group ? { license_groups: Number(license_group.id) } : {};
    const storeKey = license_group ? false : "licenses.embedded";

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: "licenses",
        sort: { field: "license_id", order: "ASC" },
        disableSyncWithLocation: false,
        storeKey: storeKey,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    localStorage.setItem("licenseembeddedlist", "true");
    localStorage.removeItem("licenseotherlist");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters(license_group)} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={showLicense}
                    bulkActionButtons={false}
                    resource="licenses"
                >
                    <TextField source="license_id" label="Id" />
                    <TextField source="name" label="Name" />
                    <BooleanField source="is_osi_approved" label="OSI approved" />
                    <BooleanField source="is_deprecated" label="Deprecated" />
                    {license_group === null && (
                        <BooleanField source="is_in_license_group" label="In license group" sortable={false} />
                    )}
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default LicenseEmbeddedList;
