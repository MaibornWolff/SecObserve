import { Stack } from "@mui/material";
import {
    BooleanField,
    Datagrid,
    FilterForm,
    Identifier,
    ListContextProvider,
    NullableBooleanInput,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { is_superuser } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import AuthorizationGroupMemberAdd from "./AuthorizationGroupMemberAdd";
import AuthorizationGroupMemberEdit from "./AuthorizationGroupMemberEdit";
import AuthorizationGroupMemberRemove from "./AuthorizationGroupMemberRemove";

function listFilters() {
    return [
        <TextInput source="full_name" alwaysOn />,
        <TextInput source="username" alwaysOn />,
        <NullableBooleanInput source="is_manager" label="Manager" alwaysOn />,
    ];
}

const showUser = (id: Identifier) => {
    return "#/users/" + id + "/show";
};

type AuthorizationGroupMemberEmbeddedListProps = {
    authorization_group: any;
};

const AuthorizationGroupMemberEmbeddedList = ({ authorization_group }: AuthorizationGroupMemberEmbeddedListProps) => {
    const listContext = useListController({
        filter: { authorization_group: Number(authorization_group.id) },
        perPage: 25,
        resource: "authorization_group_members",
        sort: { field: "user_data.full_name", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: false,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                {(is_superuser() || authorization_group.is_manager) && (
                    <AuthorizationGroupMemberAdd id={authorization_group.id} />
                )}
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false} resource="users">
                    <WithRecord
                        label="Full name"
                        render={(authorization_group_member) => (
                            <TextUrlField
                                label="User"
                                text={authorization_group_member.user_data.full_name}
                                url={showUser(authorization_group_member.user_data.id)}
                            />
                        )}
                    />
                    <WithRecord
                        label="Username"
                        render={(authorization_group_member) => (
                            <TextUrlField
                                label="User"
                                text={authorization_group_member.user_data.username}
                                url={showUser(authorization_group_member.user_data.id)}
                            />
                        )}
                    />
                    <BooleanField source="is_manager" label="Manager" />
                    {(is_superuser() || authorization_group.is_manager) && (
                        <WithRecord
                            render={(authorization_group_member) => (
                                <Stack direction="row" spacing={4}>
                                    <AuthorizationGroupMemberEdit />
                                    <AuthorizationGroupMemberRemove
                                        authorization_group_member={authorization_group_member}
                                    />
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

export default AuthorizationGroupMemberEmbeddedList;
