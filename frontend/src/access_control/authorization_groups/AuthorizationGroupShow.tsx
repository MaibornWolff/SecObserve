import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { Labeled, PrevNextButtons, Show, SimpleShowLayout, TextField, TopToolbar, WithRecord } from "react-admin";

import { useStyles } from "../../commons/layout/themes";
import UserAGEmbeddedList from "../users/UserAGEmbeddedList";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    filterDefaultValues={{ is_active: true }}
                    storeKey="authorization_groups.embedded"
                />
            </Stack>
        </TopToolbar>
    );
};

const AuthorizationGroupComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(authorization_group) => (
                <SimpleShowLayout>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Authorization Group
                        </Typography>
                        <Stack spacing={1}>
                            <Labeled label="Name">
                                <TextField source="name" className={classes.fontBigBold} />
                            </Labeled>
                            {authorization_group.oidc_group && (
                                <Labeled label="OIDC group">
                                    <TextField source="oidc_group" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Users
                        </Typography>
                        <UserAGEmbeddedList authorization_group={authorization_group} />
                    </Paper>
                </SimpleShowLayout>
            )}
        />
    );
};

const AuthorizationGroupShow = () => {
    return (
        <Show actions={<ShowActions />} component={AuthorizationGroupComponent}>
            <Fragment />
        </Show>
    );
};

export default AuthorizationGroupShow;
