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
import { PERMISSION_COMPONENT_LICENSE_EDIT } from "../../access_control/types";
import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { feature_vex_enabled, get_component_purl_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import MermaidDependencies from "../../core/observations/Mermaid_Dependencies";
import ConcludedLicense from "./ConcludedLicense";
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
                filter["branch_name_exact"] = storedFilters.storedFilters.branch_name;
            }
            if (storedFilters.storedFilters.effective_license_name) {
                filter["effective_license_name_exact"] = storedFilters.storedFilters.effective_license_name;
            }
            if (storedFilters.storedFilters.evaluation_result) {
                filter["evaluation_result"] = storedFilters.storedFilters.evaluation_result;
            }
        }
        return filter;
    };

    return (
        <TopToolbar>
            <Stack direction="row" spacing={1} alignItems="center">
                {license_component && (
                    <PrevNextButtons
                        filter={filter()}
                        queryOptions={{ meta: { api_resource: "license_component_ids" } }}
                        linkType="show"
                        sort={{ field: "evaluation_result", order: "ASC" }}
                        storeKey="license_components.embedded"
                    />
                )}
                {license_component?.permissions.includes(PERMISSION_COMPONENT_LICENSE_EDIT) && <ConcludedLicense />}
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
                        <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                            <license_components.icon />
                            &nbsp;&nbsp;License
                        </Typography>
                        <Stack spacing={2}>
                            <Stack spacing={8} direction="row">
                                {component.imported_declared_license_name === "No license information" &&
                                    component.imported_concluded_license_name === "No license information" &&
                                    component.manual_concluded_license_name === "No license information" && (
                                        <Labeled label="Effective license">
                                            <TextField
                                                source="effective_license_name"
                                                sx={{ fontStyle: "italic" }}
                                                className={classes.fontBigBold}
                                            />
                                        </Labeled>
                                    )}
                                {component.imported_declared_spdx_license && (
                                    <Labeled label="Imported declared SPDX Id">
                                        <ReferenceField
                                            source="imported_declared_spdx_license"
                                            reference="licenses"
                                            link="show"
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        >
                                            <TextField source="spdx_id_name" className={classes.fontBigBold} />
                                        </ReferenceField>
                                    </Labeled>
                                )}
                                {component.imported_declared_license_expression && (
                                    <Labeled label="Imported declared license expression">
                                        <TextField
                                            source="imported_declared_license_expression"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.imported_declared_non_spdx_license && (
                                    <Labeled label="Imported declared non-SPDX license">
                                        <TextField
                                            source="imported_declared_non_spdx_license"
                                            sx={{ fontStyle: "italic" }}
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.imported_declared_multiple_licenses && (
                                    <Labeled label="Imported declared multiple licenses">
                                        <TextField
                                            source="imported_declared_multiple_licenses"
                                            sx={{ fontStyle: "italic" }}
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {!component.imported_declared_spdx_license &&
                                    !component.imported_declared_license_expression &&
                                    !component.imported_declared_non_spdx_license &&
                                    !component.imported_declared_multiple_licenses &&
                                    component.imported_declared_license_name !== "No license information" && (
                                        <Labeled label="Imported declared license">
                                            <TextField
                                                source="imported_declared_license_name"
                                                sx={{ fontStyle: "italic" }}
                                                className={classes.fontBigBold}
                                            />
                                        </Labeled>
                                    )}
                                {component.imported_concluded_spdx_license && (
                                    <Labeled label="Imported concluded SPDX Id">
                                        <ReferenceField
                                            source="imported_concluded_spdx_license"
                                            reference="licenses"
                                            link="show"
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        >
                                            <TextField source="spdx_id_name" className={classes.fontBigBold} />
                                        </ReferenceField>
                                    </Labeled>
                                )}
                                {component.imported_concluded_license_expression && (
                                    <Labeled label="Imported concluded license expression">
                                        <TextField
                                            source="imported_concluded_license_expression"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.imported_concluded_non_spdx_license && (
                                    <Labeled label="Imported concluded non-SPDX license">
                                        <TextField
                                            source="imported_concluded_non_spdx_license"
                                            sx={{ fontStyle: "italic" }}
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.imported_concluded_multiple_licenses && (
                                    <Labeled label="Imported concluded multiple licenses">
                                        <TextField
                                            source="imported_concluded_multiple_licenses"
                                            sx={{ fontStyle: "italic" }}
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {!component.imported_concluded_spdx_license &&
                                    !component.imported_concluded_license_expression &&
                                    !component.imported_concluded_non_spdx_license &&
                                    !component.imported_concluded_multiple_licenses &&
                                    component.imported_concluded_license_name !== "No license information" && (
                                        <Labeled label="Imported concluded license">
                                            <TextField
                                                source="imported_concluded_license_name"
                                                sx={{ fontStyle: "italic" }}
                                                className={classes.fontBigBold}
                                            />
                                        </Labeled>
                                    )}
                                <Stack spacing={1}>
                                    {component.manual_concluded_spdx_license && (
                                        <Labeled label="Manual concluded SPDX Id">
                                            <ReferenceField
                                                source="manual_concluded_spdx_license"
                                                reference="licenses"
                                                link="show"
                                                sx={{ "& a": { textDecoration: "none" } }}
                                            >
                                                <TextField source="spdx_id_name" className={classes.fontBigBold} />
                                            </ReferenceField>
                                        </Labeled>
                                    )}
                                    {component.manual_concluded_license_expression && (
                                        <Labeled label="Manual concluded license expression">
                                            <TextField
                                                source="manual_concluded_license_expression"
                                                className={classes.fontBigBold}
                                            />
                                        </Labeled>
                                    )}
                                    {component.manual_concluded_non_spdx_license && (
                                        <Labeled label="Manual concluded non-SPDX license">
                                            <TextField
                                                source="manual_concluded_non_spdx_license"
                                                sx={{ fontStyle: "italic" }}
                                                className={classes.fontBigBold}
                                            />
                                        </Labeled>
                                    )}
                                    {!component.manual_concluded_spdx_license &&
                                        !component.manual_concluded_license_expression &&
                                        !component.manual_concluded_non_spdx_license &&
                                        component.manual_concluded_license_name !== "No license information" && (
                                            <Labeled label="Manual concluded license">
                                                <TextField
                                                    source="manual_concluded_license_name"
                                                    sx={{ fontStyle: "italic" }}
                                                    className={classes.fontBigBold}
                                                />
                                            </Labeled>
                                        )}
                                    {component.manual_concluded_comment && (
                                        <Labeled label="Manual concluded comment">
                                            <TextField source="manual_concluded_comment" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Stack>
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
                                            label="Name"
                                            className={classes.fontBigBold}
                                        />
                                    </Labeled>
                                )}
                                {component.component_version != "" && (
                                    <Labeled>
                                        <TextField
                                            source="component_version"
                                            label="Version"
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
                                            label="PURL"
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
                                    <TextField source="component_cpe" label="CPE" />
                                </Labeled>
                            )}
                            {feature_vex_enabled() && component.component_cyclonedx_bom_link != "" && (
                                <Labeled>
                                    <TextField source="component_cyclonedx_bom_link" label="CycloneDX BOM Link" />
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
