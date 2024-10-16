import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    Labeled,
    PrevNextButtons,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import TextUrlField from "../../commons/custom_fields/TextUrlField";
import LicenseGroupEmbeddedList from "../license_groups/LicenseGroupEmbeddedList";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "license_id", order: "ASC" }}
                    storeKey="licenses.embedded"
                />
            </Stack>
        </TopToolbar>
    );
};

const LicenseComponent = () => {
    return (
        <Stack spacing={2} sx={{ marginBottom: 1, width: "100%" }}>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Stack spacing={1}>
                    <Typography variant="h6">License</Typography>
                    <Labeled label="Id">
                        <TextField source="license_id" />
                    </Labeled>
                    <Labeled>
                        <TextField source="name" />
                    </Labeled>
                    <Labeled label="OSI approved">
                        <BooleanField source="is_osi_approved" />
                    </Labeled>
                    <Labeled label="Deprecated approved">
                        <BooleanField source="is_deprecated" />
                    </Labeled>
                    <WithRecord
                        render={(license) => (
                            <Labeled label="Reference">
                                <TextUrlField text={license.reference} url={license.reference} label="Reference" />
                            </Labeled>
                        )}
                    />
                </Stack>{" "}
            </Paper>
            <Paper sx={{ marginBottom: 1, padding: 2 }}>
                <Typography variant="h6">License Groups</Typography>
                <WithRecord render={(license) => <LicenseGroupEmbeddedList license={license} />} />
            </Paper>
        </Stack>
    );
};

const LicenseShow = () => {
    return (
        <Show actions={<ShowActions />} component={LicenseComponent}>
            <Fragment />
        </Show>
    );
};

export default LicenseShow;
