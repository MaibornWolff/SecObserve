import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { Labeled, PrevNextButtons, Show, TextField, TopToolbar, WithRecord } from "react-admin";

import LicenseEmbeddedList from "../licenses/LicenseEmbeddedList";

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
    return (
        <Stack spacing={2} sx={{ marginBottom: 1, width: "100%" }}>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Stack spacing={1}>
                    <Typography variant="h6">License Group</Typography>
                    <Labeled>
                        <TextField source="name" />
                    </Labeled>
                    <Labeled>
                        <TextField source="description" />
                    </Labeled>
                </Stack>
            </Paper>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Typography variant="h6">Licenses</Typography>
                <WithRecord render={(license_group) => <LicenseEmbeddedList license_group={license_group} />} />
            </Paper>
        </Stack>
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
