import { Box, Paper, Stack, Typography } from "@mui/material";
import { BooleanField, ChipField, DateField, Labeled, ReferenceField, TextField } from "react-admin";

import MarkdownField from "../commons/custom_fields/MarkdownField";
import TextUrlField from "../commons/custom_fields/TextUrlField";
import { feature_vex_enabled } from "../commons/functions";
import { feature_general_rules_need_approval_enabled } from "../commons/functions";
import { useStyles } from "../commons/layout/themes";
import general_rules from "./general_rules";
import product_rules from "./product_rules";

export const validateRuleForm = (values: any) => {
    const errors: any = {};

    if (!values.name) {
        errors.name = "Title is required";
    }

    if (!values.description) {
        errors.description = "Description is required";
    }

    if (!values.new_severity && !values.new_status) {
        errors.new_severity = "Either New severity or New status must be set";
        errors.new_status = "Either New severity or New status must be set";
    }

    if (!values.parser && !values.scanner_prefix) {
        errors.parser = "Either Parser or Scanner prefix must be set";
        errors.scanner_prefix = "Either Parser or Scanner prefix must be set";
    }

    return errors;
};

function generateProductURL(product_id: number, is_product_group: boolean): string {
    if (is_product_group) {
        return "#/product_groups/" + product_id + "/show/rules";
    }
    return "#/products/" + product_id + "/show/rules";
}

function getProductLabel(product_data: any): string {
    if (product_data.is_product_group) {
        return "Product group";
    }
    return "Product";
}

export const RuleShowComponent = ({ rule }: any) => {
    const { classes } = useStyles();

    return (
        <Box width={"100%"}>
            <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                {rule.product_data && (
                    <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                        <product_rules.icon />
                        &nbsp;&nbsp;Product Rule
                    </Typography>
                )}
                {!rule.product_data && (
                    <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                        <general_rules.icon />
                        &nbsp;&nbsp;General Rule
                    </Typography>
                )}
                <Stack spacing={1}>
                    {rule.product_data && (
                        <Labeled>
                            <TextUrlField
                                label={getProductLabel(rule.product_data)}
                                text={rule.product_data.name}
                                url={generateProductURL(rule.product_data.id, rule.product_data.is_product_group)}
                            />
                        </Labeled>
                    )}
                    <Labeled label="Name">
                        <TextField source="name" className={classes.fontBigBold} />
                    </Labeled>
                    {rule.description && (
                        <Labeled>
                            <MarkdownField content={rule.description} label="Description" />
                        </Labeled>
                    )}

                    {rule.new_severity && (
                        <Labeled label="New severity">
                            <TextField source="new_severity" />
                        </Labeled>
                    )}
                    {rule.new_status && (
                        <Labeled label="New status">
                            <TextField source="new_status" />
                        </Labeled>
                    )}
                    {feature_vex_enabled() && rule.new_vex_justification && (
                        <Labeled label="New VEX justification">
                            <TextField source="new_vex_justification" />
                        </Labeled>
                    )}
                    <Labeled label="Enabled">
                        <BooleanField source="enabled" />
                    </Labeled>
                    {rule.user_full_name && (
                        <Labeled label="Last changed by">
                            <TextField source="user_full_name" />
                        </Labeled>
                    )}
                </Stack>
            </Paper>

            <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Observation
                </Typography>
                <Stack spacing={1}>
                    {rule.parser && (
                        <Labeled label="Parser">
                            <ReferenceField
                                source="parser"
                                reference="parsers"
                                link="show"
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        </Labeled>
                    )}
                    {rule.scanner_prefix && (
                        <Labeled label="Scanner prefix">
                            <TextField source="scanner_prefix" />
                        </Labeled>
                    )}
                    {rule.title && (
                        <Labeled label="Title">
                            <TextField source="title" />
                        </Labeled>
                    )}
                    {rule.description_observation && (
                        <Labeled label="Description">
                            <TextField source="description_observation" />
                        </Labeled>
                    )}
                </Stack>
            </Paper>

            {rule &&
                (rule.origin_component_name_version ||
                    rule.origin_docker_image_name_tag ||
                    rule.origin_endpoint_url ||
                    rule.origin_service_name ||
                    rule.origin_source_file ||
                    rule.origin_cloud_qualified_resource ||
                    rule.origin_kubernetes_qualified_resource) && (
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Origins
                        </Typography>
                        <Stack spacing={1}>
                            {rule.origin_component_name_version && (
                                <Labeled label="Component name:version">
                                    <TextField source="origin_component_name_version" />
                                </Labeled>
                            )}
                            {rule.origin_docker_image_name_tag && (
                                <Labeled label="Docker image name:tag">
                                    <TextField source="origin_docker_image_name_tag" />
                                </Labeled>
                            )}
                            {rule.origin_endpoint_url && (
                                <Labeled label="Endpoint URL">
                                    <TextField source="origin_endpoint_url" />
                                </Labeled>
                            )}
                            {rule.origin_service_name && (
                                <Labeled label="Service name">
                                    <TextField source="origin_service_name" />
                                </Labeled>
                            )}
                            {rule.origin_source_file && (
                                <Labeled label="Source file">
                                    <TextField source="origin_source_file" />
                                </Labeled>
                            )}
                            {rule.origin_cloud_qualified_resource && (
                                <Labeled label="Cloud qualified resource">
                                    <TextField source="origin_cloud_qualified_resource" />
                                </Labeled>
                            )}
                            {rule.origin_kubernetes_qualified_resource && (
                                <Labeled label="Kubernetes qualified resource">
                                    <TextField source="origin_kubernetes_qualified_resource" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>
                )}

            {((rule.product_data &&
                (rule.product_data.product_rules_need_approval ||
                    rule.product_data.product_group_product_rules_need_approval)) ||
                (!rule.product_data && feature_general_rules_need_approval_enabled())) && (
                <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                    <Typography variant="h6" sx={{ marginBottom: 1 }}>
                        Approval
                    </Typography>
                    <Stack spacing={1}>
                        <Labeled label="Status">
                            <ChipField
                                source="approval_status"
                                sx={{
                                    width: "fit-content",
                                }}
                            />
                        </Labeled>
                        {rule.approval_user_full_name && (
                            <Labeled label="Approved/rejected by">
                                <TextField source="approval_user_full_name" />
                            </Labeled>
                        )}
                        {rule.approval_remark && (
                            <Labeled label="Approval/rejection remark">
                                <TextField source="approval_remark" />
                            </Labeled>
                        )}
                        {rule.approval_date && (
                            <Labeled label="Approval/rejection date">
                                <DateField source="approval_date" showTime />
                            </Labeled>
                        )}
                    </Stack>
                </Paper>
            )}
        </Box>
    );
};

export const non_duplicate_transform = (data: any) => {
    if (data.scanner_prefix == null) {
        data.scanner_prefix = "";
    }
    if (data.title == null) {
        data.title = "";
    }
    if (data.description_observation == null) {
        data.description_observation = "";
    }
    if (data.origin_component_name_version == null) {
        data.origin_component_name_version = "";
    }
    if (data.origin_docker_image_name_tag == null) {
        data.origin_docker_image_name_tag = "";
    }
    if (data.origin_endpoint_url == null) {
        data.origin_endpoint_url = "";
    }
    if (data.origin_service_name == null) {
        data.origin_service_name = "";
    }
    if (data.origin_source_file == null) {
        data.origin_source_file = "";
    }
    if (data.origin_cloud_qualified_resource == null) {
        data.origin_cloud_qualified_resource = "";
    }
    if (data.origin_kubernetes_qualified_resource == null) {
        data.origin_kubernetes_qualified_resource = "";
    }
    if (data.new_severity == null) {
        data.new_severity = "";
    }
    if (data.new_status == null) {
        data.new_status = "";
    }
    return data;
};
