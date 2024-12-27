import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    EditButton,
    Labeled,
    PrevNextButtons,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import MarkdownField from "../../commons/custom_fields/MarkdownField";
import { is_external, is_superuser } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import LicenseGroupAuthorizationGroupMemberEmbeddedList from "../license_group_authorization_group_members/LicenseGroupAuthorizationGroupMemberEmbeddedList";
import LicenseGroupLicenseEmbeddedList from "../license_group_licenses/LicenseGroupLicenseEmbeddedList";
import LicenseGroupMemberEmbeddedList from "../license_group_members/LicenseGroupMemberEmbeddedList";
import LicensePolicyEmbeddedList from "../license_policies/LicensePolicyEmbeddedList";
import LicenseGroupCopy from "./LicenseGroupCopy";

const ShowActions = () => {
    const license_group = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    storeKey="licensegroups.embedded"
                />
                {license_group && (!is_external() || is_superuser()) && (
                    <LicenseGroupCopy license_group={license_group} />
                )}
                {((license_group && license_group.is_manager) || is_superuser()) && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const LicenseGroupComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(license_group) => (
                <Stack spacing={2} sx={{ marginBottom: 1, width: "100%" }}>
                    <Paper sx={{ marginBottom: 1, padding: 2 }}>
                        <Stack spacing={1}>
                            <Typography variant="h6">License Group</Typography>
                            <Labeled>
                                <TextField source="name" className={classes.fontBigBold} />
                            </Labeled>
                            <Labeled>
                                <MarkdownField content={license_group.description} label="Description" />
                            </Labeled>
                            <Labeled label="Public">
                                <BooleanField source="is_public" />
                            </Labeled>
                        </Stack>
                    </Paper>
                    <Paper sx={{ marginBottom: 1, padding: 2 }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>Licenses</Typography>
                        <LicenseGroupLicenseEmbeddedList license_group={license_group} />
                    </Paper>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Users
                        </Typography>
                        <LicenseGroupMemberEmbeddedList license_group={license_group} />
                    </Paper>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Authorization Groups
                        </Typography>
                        <LicenseGroupAuthorizationGroupMemberEmbeddedList license_group={license_group} />
                    </Paper>
                    {license_group.is_in_license_policy && (
                        <Paper sx={{ marginBottom: 1, padding: 2 }}>
                            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                                License Policies containing this license group
                            </Typography>
                            <LicensePolicyEmbeddedList license={null} license_group={license_group} />
                        </Paper>
                    )}
                </Stack>
            )}
        />
    );
};

const LicenseGroupShow = () => {
    return (
        <Show actions={<ShowActions />} component={LicenseGroupComponent}>
            <Fragment />
        </Show>
    );
};

export default LicenseGroupShow;
