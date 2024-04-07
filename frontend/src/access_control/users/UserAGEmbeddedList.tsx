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
import { getSettingListSize } from "../../commons/settings/functions";
import AuthorizationGroupUserAdd from "../authorization_groups/AuthorizationGroupUserAdd";
import AuthorizationGroupUserRemove from "../authorization_groups/AuthorizationGroupUserRemove";

function listFilters() {
    return [
        <TextInput source="username" alwaysOn />,
        <TextInput source="full_name" alwaysOn />,
        <NullableBooleanInput source="is_active" label="Active" alwaysOn />,
        <NullableBooleanInput source="is_external" label="External" alwaysOn />,
        <NullableBooleanInput source="is_superuser" label="Superuser" alwaysOn />,
    ];
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

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    localStorage.setItem("useragembeddedlist", "true");
    localStorage.removeItem("userembeddedlist");
    localStorage.setItem("useragembeddedlist.authorization_group", authorization_group.id);

    const user = localStorage.getItem("user");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                {user && JSON.parse(user).is_superuser && <AuthorizationGroupUserAdd id={authorization_group.id} />}
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false}>
                    <TextField source="username" />
                    <TextField source="full_name" />
                    <BooleanField source="is_active" label="Active" />
                    <BooleanField source="is_external" label="External" />
                    <BooleanField source="is_superuser" label="Superuser" />
                    {user && JSON.parse(user).is_superuser && (
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
