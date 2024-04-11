import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    DateField,
    EditButton,
    Labeled,
    PrevNextButtons,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { is_superuser } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import UserChangePassword from "./UserChangePassword";

const ShowActions = () => {
    const current_user = localStorage.getItem("user");
    const user = useRecordContext();

    let filter = null;
    let storeKey = null;

    if (localStorage.getItem("userembeddedlist")) {
        filter = {};
        storeKey = "users.embedded";
    }
    if (localStorage.getItem("useragembeddedlist")) {
        filter = { authorization_group: localStorage.getItem("useragembeddedlist.authorization_group") };
        storeKey = "users.agembedded";
    }

    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {filter && storeKey && (
                    <PrevNextButtons
                        linkType="show"
                        filter={filter}
                        sort={{ field: "username", order: "ASC" }}
                        filterDefaultValues={{ is_active: true }}
                        storeKey={storeKey}
                    />
                )}
                {user &&
                    !user.is_oidc_user &&
                    (is_superuser() || (current_user && user && JSON.parse(current_user).id == user.id)) && (
                        <UserChangePassword />
                    )}
                {is_superuser() && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const UserComponent = () => {
    const { classes } = useStyles();
    const current_user = localStorage.getItem("user");

    return (
        <WithRecord
            render={(user) => (
                <SimpleShowLayout>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            User
                        </Typography>
                        <Stack spacing={1}>
                            <Labeled label="Username">
                                <TextField source="username" className={classes.fontBigBold} />
                            </Labeled>
                            <Labeled label="Full name">
                                <TextField source="full_name" />
                            </Labeled>
                            {user.first_name && (
                                <Labeled label="First name">
                                    <TextField source="first_name" />
                                </Labeled>
                            )}
                            {user.last_name && (
                                <Labeled label="Last name">
                                    <TextField source="last_name" />
                                </Labeled>
                            )}
                            {user.email && (
                                <Labeled label="Email">
                                    <TextField source="email" />
                                </Labeled>
                            )}
                            {user.date_joined && (
                                <Labeled label="Created">
                                    <DateField source="date_joined" showTime />
                                </Labeled>
                            )}
                            {user.has_password != undefined && (
                                <Labeled label="Has password">
                                    <BooleanField source="has_password" />
                                </Labeled>
                            )}
                            {user.is_oidc_user != undefined && (
                                <Labeled label="OIDC user">
                                    <BooleanField source="is_oidc_user" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>
                    {(is_superuser() || (current_user && JSON.parse(current_user).id == user.id)) && (
                        <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Permissions
                            </Typography>
                            <Stack spacing={1}>
                                <Labeled label="Active">
                                    <BooleanField source="is_active" />
                                </Labeled>
                                <Labeled label="External">
                                    <BooleanField source="is_external" />
                                </Labeled>
                                <Labeled label="Superuser">
                                    <BooleanField source="is_superuser" />
                                </Labeled>
                            </Stack>
                        </Paper>
                    )}
                    {(is_superuser() || (current_user && JSON.parse(current_user).id == user.id)) && (
                        <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Settings
                            </Typography>
                            <Stack spacing={1}>
                                {user.setting_theme && (
                                    <Labeled label="Theme">
                                        <TextField source="setting_theme" />
                                    </Labeled>
                                )}
                                {user.setting_list_size && (
                                    <Labeled label="List size">
                                        <TextField source="setting_list_size" />
                                    </Labeled>
                                )}
                            </Stack>
                        </Paper>
                    )}
                </SimpleShowLayout>
            )}
        />
    );
};

const UserShow = () => {
    return (
        <Show actions={<ShowActions />} component={UserComponent}>
            <Fragment />
        </Show>
    );
};

export default UserShow;
