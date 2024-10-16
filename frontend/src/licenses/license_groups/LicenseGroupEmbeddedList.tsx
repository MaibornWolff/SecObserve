import { Datagrid, FilterForm, ListContextProvider, TextField, TextInput, useListController } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";

const showLicenseGroup = (id: any) => {
    return "../../../../license_groups/" + id + "/show";
};

const listFilters = [<TextInput source="name" alwaysOn />];

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

    localStorage.setItem("licensegroupembeddedlist", "true");
    localStorage.removeItem("licensegroupotherlist");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={showLicenseGroup}
                    bulkActionButtons={false}
                    resource="license_groups"
                >
                    <TextField source="name" label="Name" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default LicenseGroupEmbeddedList;
