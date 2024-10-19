import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { BooleanField, Labeled, PrevNextButtons, Show, TextField, TopToolbar, WithRecord } from "react-admin";

import TextUrlField from "../../commons/custom_fields/TextUrlField";
import LicenseGroupEmbeddedList from "../license_groups/LicenseGroupEmbeddedList";
import { useStyles } from "../../commons/layout/themes";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "spdx_id", order: "ASC" }}
                    storeKey="licenses.embedded"
                />
            </Stack>
        </TopToolbar>
    );
};

const LicenseComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(license) => (
                <Stack spacing={2} sx={{ marginBottom: 1, width: "100%" }}>
                    <Paper sx={{ marginBottom: 1, padding: 2 }}>
                        <Stack spacing={1}>
                            <Typography variant="h6">License</Typography>
                            <Labeled label="SPDX Id">
                                <TextField source="spdx_id" className={classes.fontBigBold} />
                            </Labeled>
                            <Labeled>
                                <TextField source="name" />
                            </Labeled>
                            <Labeled label="OSI approved">
                                <BooleanField source="is_osi_approved" />
                            </Labeled>
                            <Labeled label="Deprecated">
                                <BooleanField source="is_deprecated" />
                            </Labeled>
                            <WithRecord
                                render={(license) => (
                                    <Labeled label="Reference">
                                        <TextUrlField
                                            text={license.reference}
                                            url={license.reference}
                                            label="Reference"
                                        />
                                    </Labeled>
                                )}
                            />
                        </Stack>{" "}
                    </Paper>
                    {license.is_in_license_group && (
                        <Paper sx={{ marginBottom: 1, padding: 2 }}>
                            <Typography variant="h6" sx={{marginBottom: 2}}>License Groups</Typography>
                            <WithRecord render={(license) => <LicenseGroupEmbeddedList license={license} />} />
                        </Paper>
                    )}
                </Stack>
            )}
        />
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
