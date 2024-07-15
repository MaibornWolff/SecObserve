import {
    BooleanField,
    Datagrid,
    FilterForm,
    ListContextProvider,
    NullableBooleanInput,
    TextField,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { is_superuser } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import AuthorizationGroupUserAdd from "../authorization_groups/AuthorizationGroupUserAdd";
import AuthorizationGroupUserRemove from "../authorization_groups/AuthorizationGroupUserRemove";

function listFilters() {
    if (is_superuser()) {
        return [
            <TextInput source="username" alwaysOn />,
            <TextInput source="full_name" alwaysOn />,
            <NullableBooleanInput source="is_active" label="Active" alwaysOn />,
            <NullableBooleanInput source="is_oidc_user" label="OIDC user" alwaysOn />,
            <NullableBooleanInput source="is_external" label="External" alwaysOn />,
            <NullableBooleanInput source="is_superuser" label="Superuser" alwaysOn />,
        ];
    } else {
        return [<TextInput source="username" alwaysOn />, <TextInput source="full_name" alwaysOn />];
    }
}

type UserAGEmbeddedListProps = {
    authorization_group: any;
};

const UserAGEmbeddedList = ({ authorization_group }: UserAGEmbeddedListProps) => {
    const listContext = useListController({
        filter: { authorization_group: Number(authorization_group.id) },
        perPage: 25,
        resource: "users",
        sort: { field: "username", order: "ASC" },
        filterDefaultValues: { is_active: true },
        disableSyncWithLocation: false,
        storeKey: "users.agembedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    localStorage.setItem("useragembeddedlist", "true");
    localStorage.removeItem("userembeddedlist");
    localStorage.setItem("useragembeddedlist.authorization_group", authorization_group.id);

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                {is_superuser() && <AuthorizationGroupUserAdd id={authorization_group.id} />}
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false} resource="users">
                    <TextField source="username" />
                    <TextField source="full_name" sx={{ wordBreak: "break-word" }} />
                    {is_superuser() && <BooleanField source="is_active" label="Active" />}
                    {is_superuser() && <BooleanField source="is_oidc_user" label="OIDC user" />}
                    {is_superuser() && <BooleanField source="is_external" label="External" />}
                    {is_superuser() && <BooleanField source="is_superuser" label="Superuser" />}
                    {is_superuser() && (
                        <WithRecord
                            render={(user) => <AuthorizationGroupUserRemove id={authorization_group.id} user={user} />}
                        />
                    )}
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default UserAGEmbeddedList;
