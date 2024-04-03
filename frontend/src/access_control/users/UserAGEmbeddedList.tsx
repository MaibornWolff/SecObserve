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
import { getSettingListSize } from "../../commons/settings/functions";

const ShowUsers = (id: any) => {
    return "../../../../users/" + id + "/show";
};

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

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} rowClick={ShowUsers} bulkActionButtons={false}>
                    <TextField source="username" />
                    <TextField source="full_name" />
                    <BooleanField source="is_active" label="Active" />
                    <BooleanField source="is_external" label="External" />
                    <BooleanField source="is_superuser" label="Superuser" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default UserAGEmbeddedList;
