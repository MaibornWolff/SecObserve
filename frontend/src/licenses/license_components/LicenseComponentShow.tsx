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

import license_components from ".";
import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_component_purl_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import MermaidDependencies from "../../core/observations/Mermaid_Dependencies";
import LicenseComponentShowAside from "./LicenseComponentShowAside";

const ShowActions = () => {
    const license_component = useRecordContext();

    const filter = () => {
        // eslint-disable-next-line @typescript-eslint/consistent-indexed-object-style
        const filter: { [key: string]: any } = {};
        if (license_component) {
            filter["product"] = Number(license_component.product);
        }
        const license_component_expand_filters = localStorage.getItem("license_component_expand_filters");
        const storedFilters = license_component_expand_filters ? JSON.parse(license_component_expand_filters) : {};
        if (storedFilters.storedFilters) {
            if (storedFilters.storedFilters.branch_name) {
                filter["branch_name"] = storedFilters.storedFilters.branch_name;
            }
            if (storedFilters.storedFilters.license_name) {
                filter["license_name_exact"] = storedFilters.storedFilters.license_name;
            }
            if (storedFilters.storedFilters.evaluation_result) {
                filter["evaluation_result"] = storedFilters.storedFilters.evaluation_result;
            }
        }
        return filter;
    };

    return (
        <TopToolbar>
            {license_component && (
                <PrevNextButtons
                    filter={filter()}
                    queryOptions={{ meta: { api_resource: "license_component_ids" } }}
                    linkType="show"
                    sort={{ field: "evaluation_result", order: "ASC" }}
                    storeKey="license_components.embedded"
                />
            )}
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
                        <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                            <license_components.icon />
                            &nbsp;&nbsp;License
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
                            {component.license_expression && (
                                <Labeled label="License expression">
                                    <TextField source="license_expression" className={classes.fontBigBold} />
                                </Labeled>
                            )}
                            {component.non_spdx_license && (
                                <Labeled label="Non-SPDX license">
                                    <TextField
                                        source="non_spdx_license"
                                        sx={{ fontStyle: "italic" }}
                                        className={classes.fontBigBold}
                                    />
                                </Labeled>
                            )}
                            {component.multiple_licenses && (
                                <Labeled label="Multiple licenses">
                                    <TextField
                                        source="multiple_licenses"
                                        sx={{ fontStyle: "italic" }}
                                        className={classes.fontBigBold}
                                    />
                                </Labeled>
                            )}
                            {!component.license &&
                                !component.license_expression &&
                                !component.non_spdx_license &&
                                !component.multiple_licenses && (
                                    <Labeled label="License">
                                        <TextField
                                            source="license_name"
                                            sx={{ fontStyle: "italic" }}
                                            className={classes.fontBigBold}
                                        />
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
                                {component.component_name != "" && (
                                    <Labeled>
                                        <TextField
                                            source="component_name"
                                            label="Component name"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.component_version != "" && (
                                    <Labeled>
                                        <TextField
                                            source="component_version"
                                            label="Component version"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                            </Stack>
                            {component.component_purl != "" &&
                                get_component_purl_url(
                                    component.component_name,
                                    component.component_version,
                                    component.component_purl_type,
                                    component.component_purl_namespace
                                ) == null && (
                                    <Labeled>
                                        <TextField source="component_purl" label="Component PURL" />
                                    </Labeled>
                                )}
                            {component.component_purl != "" &&
                                get_component_purl_url(
                                    component.component_name,
                                    component.component_version,
                                    component.component_purl_type,
                                    component.component_purl_namespace
                                ) != null && (
                                    <Labeled>
                                        <TextUrlField
                                            label="Component PURL"
                                            text={component.component_purl}
                                            url={
                                                component.component_purl &&
                                                get_component_purl_url(
                                                    component.component_name,
                                                    component.component_version,
                                                    component.component_purl_type,
                                                    component.component_purl_namespace
                                                )
                                            }
                                            new_tab={true}
                                        />
                                    </Labeled>
                                )}
                            {component.component_cpe != "" && (
                                <Labeled>
                                    <TextField source="component_cpe" label="Component CPE" />
                                </Labeled>
                            )}
                            {component.component_dependencies && component.component_dependencies != "" && (
                                <MermaidDependencies dependencies={component.component_dependencies} />
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
