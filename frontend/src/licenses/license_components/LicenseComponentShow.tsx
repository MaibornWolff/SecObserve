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
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_component_purl_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import MermaidDependencies from "../../core/observations/Mermaid_Dependencies";
import LicenseComponentShowAside from "./LicenseComponentShowAside";

const ShowActions = () => {
    const component = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {component && (
                    <PrevNextButtons
                        filter={{
                            product: Number(component.product),
                        }}
                        queryOptions={{ meta: { api_resource: "license_component_ids" } }}
                        linkType="show"
                        sort={{ field: "evaluation_result", order: "ASC" }}
                        storeKey="license_components.embedded"
                    />
                )}
            </Stack>
        </TopToolbar>
    );
};

export const LicenseComponentComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(component) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            License
                        </Typography>
                        <Stack spacing={1}>
                            {component.license && (
                                <Stack direction="row" spacing={4}>
                                    <Labeled label="SPDX Id">
                                        <ReferenceField
                                            source="license"
                                            reference="licenses"
                                            link="show"
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        >
                                            <TextField source="spdx_id" className={classes.fontBigBold} />
                                        </ReferenceField>
                                    </Labeled>
                                    <Labeled label="Name">
                                        <TextField source="license_data.name" className={classes.fontBigBold} />
                                    </Labeled>
                                </Stack>
                            )}
                            {component.unknown_license && (
                                <Labeled label="Unknown license">
                                    <TextField source="unknown_license" className={classes.fontBigBold} />
                                </Labeled>
                            )}
                            <Labeled label="Evaluation result">
                                <EvaluationResultField source="evaluation_result" label="Evaluation result" />
                            </Labeled>
                        </Stack>
                    </Paper>
                    <Paper sx={{ marginBottom: 1, padding: 2 }}>
                        <Stack spacing={1}>
                            <Typography variant="h6">Component</Typography>
                            <Stack direction="row" spacing={4}>
                                {component.name != "" && (
                                    <Labeled>
                                        <TextField
                                            source="name"
                                            label="Component name"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.version != "" && (
                                    <Labeled>
                                        <TextField
                                            source="version"
                                            label="Component version"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                            </Stack>
                            {component.purl != "" &&
                                get_component_purl_url(
                                    component.name,
                                    component.version,
                                    component.purl_type,
                                    component.purl_namespace
                                ) == null && (
                                    <Labeled>
                                        <TextField source="purl" label="Component PURL" />
                                    </Labeled>
                                )}
                            {component.purl != "" &&
                                get_component_purl_url(
                                    component.name,
                                    component.version,
                                    component.purl_type,
                                    component.purl_namespace
                                ) != null && (
                                    <Labeled>
                                        <TextUrlField
                                            label="Component PURL"
                                            text={component.purl}
                                            url={
                                                component.purl &&
                                                get_component_purl_url(
                                                    component.name,
                                                    component.version,
                                                    component.purl_type,
                                                    component.purl_namespace
                                                )
                                            }
                                        />
                                    </Labeled>
                                )}
                            {component.cpe != "" && (
                                <Labeled>
                                    <TextField source="cpe" label="Component CPE" />
                                </Labeled>
                            )}
                            {component.dependencies && component.dependencies != "" && (
                                <MermaidDependencies dependencies={component.dependencies} />
                            )}
                        </Stack>
                    </Paper>
                </Box>
            )}
        />
    );
};

const LicenseComponentShow = () => {
    return (
        <Show actions={<ShowActions />} component={LicenseComponentComponent} aside={<LicenseComponentShowAside />}>
            <Fragment />
        </Show>
    );
};

export default LicenseComponentShow;
