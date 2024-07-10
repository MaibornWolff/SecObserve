import { Datagrid, FilterForm, ListContextProvider, TextField, TextInput, useListController } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { is_superuser } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import AuthorizationGroupCreateButton from "./AuthorizationGroupCreateButton";

const ShowAuthorizationGroups = (id: any) => {
    return "../../../../authorization_groups/" + id + "/show";
};

function listFilters() {
    return [<TextInput source="name" alwaysOn />, <TextInput source="oidc_group" label="OIDC group" alwaysOn />];
}

const AuthorizationGroupEmbeddedList = () => {
    const listContext = useListController({
        filter: {},
        perPage: 25,
        resource: "authorization_groups",
        sort: { field: "name", order: "ASC" },
        filterDefaultValues: { is_active: true },
        disableSyncWithLocation: false,
        storeKey: "authorization_groups.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                {is_superuser() && <AuthorizationGroupCreateButton />}
                <FilterForm filters={listFilters()} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={ShowAuthorizationGroups}
                    bulkActionButtons={false}
                    resource="authorization_groups"
                >
                    <TextField source="name" />
                    <TextField source="oidc_group" label="OIDC group" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default AuthorizationGroupEmbeddedList;
