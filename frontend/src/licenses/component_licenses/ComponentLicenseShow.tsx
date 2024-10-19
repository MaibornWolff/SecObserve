import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    Labeled,
    PrevNextButtons,
    ReferenceField,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import { useStyles } from "../../commons/layout/themes";
import ComponentEmbeddedList from "../components/ComponentEmbeddedList";

const ShowActions = () => {
    const component_license = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {component_license && (
                    <PrevNextButtons
                        filter={{ product: Number(component_license.vulnerability_check_data.product) }}
                        linkType="show"
                        sort={{ field: "license_spdx_id", order: "ASC" }}
                        storeKey="component_licenses.embedded"
                    />
                )}
            </Stack>
        </TopToolbar>
    );
};

const ComponentLicenseComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(component_license) => (
                <Box width={"100%"}>
                    <Stack direction="row" spacing={2} sx={{ marginBottom: 2 }}>
                        <Stack spacing={2} sx={{ marginBottom: 1, width: "50%" }}>
                            <Paper sx={{ marginBottom: 1, padding: 2, height: "100%" }}>
                                <Stack spacing={1}>
                                    <Typography variant="h6">License</Typography>
                                    {component_license.license_spdx_id && (
                                        <Labeled label="License">
                                            <ReferenceField
                                                source="license"
                                                reference="licenses"
                                                link="show"
                                                sx={{ "& a": { textDecoration: "none" } }}
                                            >
                                                <TextField source="spdx_id" className={classes.fontBigBold} />
                                            </ReferenceField>
                                        </Labeled>
                                    )}
                                    {component_license.unknown_license && (
                                        <Labeled label="Unknown license">
                                            <TextField source="unknown_license" />
                                        </Labeled>
                                    )}
                                    <Labeled label="Evaluation result">
                                        <EvaluationResultField source="evaluation_result" label="Evaluation result" />
                                    </Labeled>
                                </Stack>
                            </Paper>
                        </Stack>
                        <Stack spacing={2} sx={{ marginBottom: 1, width: "50%" }}>
                            <Paper sx={{ marginBottom: 1, padding: 2, height: "100%" }}>
                                <Stack spacing={1}>
                                    <Typography variant="h6">Metadata</Typography>
                                    <Labeled label="Product">
                                        <ReferenceField
                                            source="vulnerability_check_data.product"
                                            reference="products"
                                            link="show"
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        />
                                    </Labeled>
                                    {component_license.vulnerability_check_data.branch_name && (
                                        <Labeled label="Branch">
                                            <TextField source="vulnerability_check_data.branch_name" />
                                        </Labeled>
                                    )}
                                    {component_license.vulnerability_check_data.filename != "" && (
                                        <Labeled label="Upload filename">
                                            <TextField source="vulnerability_check_data.filename" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Paper>
                        </Stack>
                    </Stack>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Components
                        </Typography>
                        <ComponentEmbeddedList component_license={component_license} />
                    </Paper>
                </Box>
            )}
        />
    );
};

const ComponentLicenseShow = () => {
    return (
        <Show actions={<ShowActions />} component={ComponentLicenseComponent}>
            <Fragment />
        </Show>
    );
};

export default ComponentLicenseShow;
