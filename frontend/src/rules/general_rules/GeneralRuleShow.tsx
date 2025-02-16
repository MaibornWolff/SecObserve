import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    ChipField,
    DateField,
    EditButton,
    Labeled,
    PrevNextButtons,
    ReferenceField,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import general_rules from ".";
import MarkdownField from "../../commons/custom_fields/MarkdownField";
import { feature_vex_enabled } from "../../commons/functions";
import { is_superuser } from "../../commons/functions";
import { feature_general_rules_need_approval_enabled } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import RuleApproval from "../RuleApproval";
import { RULE_STATUS_NEEDS_APPROVAL } from "../types";

const ShowActions = () => {
    const rule = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons linkType="show" sort={{ field: "name", order: "ASC" }} storeKey="general_rules.list" />
                {rule &&
                    rule.approval_status == RULE_STATUS_NEEDS_APPROVAL &&
                    feature_general_rules_need_approval_enabled() &&
                    is_superuser() && <RuleApproval rule_id={rule.id} class="general_rules" />}
                {is_superuser() && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const GeneralRuleComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(rule) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                            <general_rules.icon />
                            &nbsp;&nbsp;General Rule
                        </Typography>
                        <Stack spacing={1}>
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

                    {feature_general_rules_need_approval_enabled() && (
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
            )}
        />
    );
};

const GeneralRuleShow = () => {
    return (
        <Show actions={<ShowActions />} component={GeneralRuleComponent}>
            <Fragment />
        </Show>
    );
};

export default GeneralRuleShow;
