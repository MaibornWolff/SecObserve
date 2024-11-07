import { Stack } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    Datagrid,
    FilterForm,
    Identifier,
    ListContextProvider,
    NullableBooleanInput,
    ResourceContextProvider,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { is_superuser } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import LicenseGroupMemberAdd from "./LicenseGroupMemberAdd";
import LicenseGroupMemberEdit from "./LicenseGroupMemberEdit";
import LicenseGroupMemberRemove from "./LicenseGroupMemberRemove";

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

type LicenseGroupMemberEmbeddedListProps = {
    license_group: any;
};

const LicenseGroupMemberEmbeddedList = ({ license_group }: LicenseGroupMemberEmbeddedListProps) => {
    const listContext = useListController({
        filter: { license_group: Number(license_group.id) },
        perPage: 25,
        resource: "license_group_members",
        sort: { field: "user_data.full_name", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: true,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="license_group_members">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    {(is_superuser() || license_group.is_manager) && <LicenseGroupMemberAdd id={license_group.id} />}
                    {license_group.has_users && (
                        <Fragment>
                            <FilterForm filters={listFilters()} />
                            <Datagrid
                                size={getSettingListSize()}
                                rowClick={false}
                                bulkActionButtons={false}
                                resource="users"
                            >
                                <WithRecord
                                    label="Full name"
                                    render={(license_group_member) => (
                                        <TextUrlField
                                            label="User"
                                            text={license_group_member.user_data.full_name}
                                            url={showUser(license_group_member.user_data.id)}
                                        />
                                    )}
                                />
                                <WithRecord
                                    label="Username"
                                    render={(license_group_member) => (
                                        <TextUrlField
                                            label="User"
                                            text={license_group_member.user_data.username}
                                            url={showUser(license_group_member.user_data.id)}
                                        />
                                    )}
                                />
                                <BooleanField source="is_manager" label="Manager" />
                                {(is_superuser() || license_group.is_manager) && (
                                    <WithRecord
                                        render={(license_group_member) => (
                                            <Stack direction="row" spacing={4}>
                                                <LicenseGroupMemberEdit />
                                                <LicenseGroupMemberRemove license_group_member={license_group_member} />
                                            </Stack>
                                        )}
                                    />
                                )}
                            </Datagrid>
                            <CustomPagination />
                        </Fragment>
                    )}
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default LicenseGroupMemberEmbeddedList;
