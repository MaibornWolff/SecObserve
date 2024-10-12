import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    EditButton,
    Labeled,
    PrevNextButtons,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { useStyles } from "../../commons/layout/themes";
import UserProductAuthorizationGroupMemberEmbeddedList from "../../core/product_authorization_group_members/UserProductAuthorizationGroupMemberEmbeddedList";
import AuthorizationGroupMemberEmbeddedList from "../authorization_group_members/AuthorizationGroupMemberEmbeddedList";

const ShowActions = () => {
    const authorization_group = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    filterDefaultValues={{ is_active: true }}
                    storeKey="authorization_groups.embedded"
                />
                {authorization_group && authorization_group.is_manager && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const AuthorizationGroupComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(authorization_group) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
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
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Users
                        </Typography>
                        <AuthorizationGroupMemberEmbeddedList authorization_group={authorization_group} />
                    </Paper>
                    {authorization_group.has_product_group_members && (
                        <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Product Groups
                            </Typography>
                            <UserProductAuthorizationGroupMemberEmbeddedList
                                authorization_group={authorization_group}
                                is_product_group={true}
                            />
                        </Paper>
                    )}
                    {authorization_group.has_product_members && (
                        <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Products
                            </Typography>
                            <UserProductAuthorizationGroupMemberEmbeddedList
                                authorization_group={authorization_group}
                                is_product_group={false}
                            />
                        </Paper>
                    )}
                </Box>
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
