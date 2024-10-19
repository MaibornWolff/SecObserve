import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { Labeled, PrevNextButtons, Show, TextField, TopToolbar, WithRecord } from "react-admin";

import LicenseEmbeddedList from "../licenses/LicenseEmbeddedList";
import { useStyles } from "../../commons/layout/themes";
import MarkdownField from "../../commons/custom_fields/MarkdownField";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    storeKey="licensegroups.embedded"
                />
            </Stack>
        </TopToolbar>
    );
};

const LicenseGroupComponent = () => {
    const { classes } = useStyles();

    return (
<WithRecord render={(license_group) =>         <Stack spacing={2} sx={{ marginBottom: 1, width: "100%" }}>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Stack spacing={1}>
                    <Typography variant="h6">License Group</Typography>
                    <Labeled>
                        <TextField source="name" className={classes.fontBigBold} />
                    </Labeled>
                    <Labeled>
                        <MarkdownField content={license_group.description} label="Description" />
                    </Labeled>
                </Stack>
            </Paper>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Typography variant="h6">Licenses</Typography>
                <LicenseEmbeddedList license_group={license_group} />
            </Paper>
        </Stack>} />
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
