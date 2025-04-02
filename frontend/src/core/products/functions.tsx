import { Divider, Stack, Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import { Fragment } from "react";
import {
    BooleanInput,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    ReferenceInput,
    WithRecord,
} from "react-admin";

import products from ".";
import OSVLinuxDistributionInput from "../../commons/custom_fields/OSVLinuxDistributionInput";
import { validate_0_999999, validate_255, validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { feature_automatic_osv_scanning, feature_license_management } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { ISSUE_TRACKER_TYPE_CHOICES, OBSERVATION_SEVERITY_CHOICES } from "../types";

export const transform = (data: any) => {
    if (!data.description) {
        data.description = "";
    }
    if (!data.purl) {
        data.purl = "";
    }
    if (!data.cpe23) {
        data.cpe23 = "";
    }
    if (!data.repository_prefix) {
        data.repository_prefix = "";
    }
    if (data.repository_branch_housekeeping_active) {
        if (data.repository_branch_housekeeping_keep_inactive_days == "") {
            data.repository_branch_housekeeping_keep_inactive_days = 1;
        }
    } else {
        if (data.repository_branch_housekeeping_keep_inactive_days == "") {
            data.repository_branch_housekeeping_keep_inactive_days = null;
        }
    }
    if (!data.repository_branch_housekeeping_exempt_branches) {
        data.repository_branch_housekeeping_exempt_branches = "";
    }
    if (!data.notification_email_to) {
        data.notification_email_to = "";
    }
    if (!data.notification_ms_teams_webhook) {
        data.notification_ms_teams_webhook = "";
    }
    if (!data.notification_slack_webhook) {
        data.notification_slack_webhook = "";
    }
    if (data.security_gate_active) {
        if (data.security_gate_threshold_critical == "") {
            data.security_gate_threshold_critical = 0;
        }
        if (data.security_gate_threshold_high == "") {
            data.security_gate_threshold_high = 0;
        }
        if (data.security_gate_threshold_medium == "") {
            data.security_gate_threshold_medium = 0;
        }
        if (data.security_gate_threshold_low == "") {
            data.security_gate_threshold_low = 0;
        }
        if (data.security_gate_threshold_none == "") {
            data.security_gate_threshold_none = 0;
        }
        if (data.security_gate_threshold_unknown == "") {
            data.security_gate_threshold_unknown = 0;
        }
    } else {
        if (data.security_gate_threshold_critical == "") {
            data.security_gate_threshold_critical = null;
        }
        if (data.security_gate_threshold_high == "") {
            data.security_gate_threshold_high = null;
        }
        if (data.security_gate_threshold_medium == "") {
            data.security_gate_threshold_medium = null;
        }
        if (data.security_gate_threshold_low == "") {
            data.security_gate_threshold_low = null;
        }
        if (data.security_gate_threshold_none == "") {
            data.security_gate_threshold_none = null;
        }
        if (data.security_gate_threshold_unknown == "") {
            data.security_gate_threshold_unknown = null;
        }
    }
    if (!data.issue_tracker_type) {
        data.issue_tracker_type = "";
    }
    if (!data.issue_tracker_base_url) {
        data.issue_tracker_base_url = "";
    }
    if (!data.issue_tracker_api_key) {
        data.issue_tracker_api_key = "";
    }
    if (!data.issue_tracker_project_id) {
        data.issue_tracker_project_id = "";
    }
    if (!data.issue_tracker_labels) {
        data.issue_tracker_labels = "";
    }
    if (!data.issue_tracker_username) {
        data.issue_tracker_username = "";
    }
    if (!data.issue_tracker_issue_type) {
        data.issue_tracker_issue_type = "";
    }
    if (!data.issue_tracker_status_closed) {
        data.issue_tracker_status_closed = "";
    }
    if (!data.issue_tracker_minimum_severity) {
        data.issue_tracker_minimum_severity = "";
    }
    if (data.risk_acceptance_expiry_active) {
        if (data.risk_acceptance_expiry_days == "") {
            data.risk_acceptance_expiry_days = 30;
        }
    } else {
        if (data.risk_acceptance_expiry_days == "") {
            data.risk_acceptance_expiry_days = null;
        }
    }
    if (!data.osv_enabled) {
        data.osv_linux_distribution = "";
        data.osv_linux_release = "";
        data.automatic_osv_scanning_enabled = false;
    }
    if (!data.osv_linux_distribution) {
        data.osv_linux_distribution = "";
    }
    if (!data.osv_linux_release) {
        data.osv_linux_release = "";
    }
    return data;
};

export type ProductCreateEditComponentProps = {
    edit: boolean;
};

export const ProductCreateEditComponent = ({ edit }: ProductCreateEditComponentProps) => {
    return (
        <Fragment>
            <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                <products.icon />
                &nbsp;&nbsp;Product
            </Typography>
            <TextInputWide autoFocus source="name" validate={validate_required_255} />
            <RichTextInput source="description" validate={validate_2048} />
            <ReferenceInput
                source="product_group"
                reference="product_groups"
                queryOptions={{ meta: { api_resource: "product_group_names" } }}
                sort={{ field: "name", order: "ASC" }}
            >
                <AutocompleteInputWide optionText="name" />
            </ReferenceInput>
            <Stack direction="row" spacing={4}>
                <TextInputWide source="purl" validate={validate_255} label="PURL" />
                <TextInputWide source="cpe23" validate={validate_255} label="CPE 2.3" />
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                Rules
            </Typography>
            <BooleanInput source="apply_general_rules" defaultValue={true} />

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                Source code repository and housekeeping
            </Typography>
            <TextInputWide
                source="repository_prefix"
                helperText="URL prefix to link to a file in the source code repository"
                validate={validate_255}
            />
            {edit && (
                <WithRecord
                    render={(product) => (
                        <ReferenceInput
                            source="repository_default_branch"
                            reference="branches"
                            queryOptions={{ meta: { api_resource: "branch_names" } }}
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ product: product.id }}
                        >
                            <AutocompleteInputWide optionText="name" label="Default branch / version" />
                        </ReferenceInput>
                    )}
                />
            )}
            <Stack direction="row" spacing={4}>
                <NullableBooleanInput
                    source="repository_branch_housekeeping_active"
                    label="Housekeeping"
                    defaultValue={null}
                    nullLabel="Standard"
                    falseLabel="Disabled"
                    trueLabel="Product specific"
                    helperText="Delete inactive branches / versions"
                    sx={{ marginBottom: 2 }}
                />
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.repository_branch_housekeeping_active && (
                            <Fragment>
                                <NumberInput
                                    source="repository_branch_housekeeping_keep_inactive_days"
                                    label="Keep inactive"
                                    helperText="Days before inactive branches / versions and their observations are deleted"
                                    defaultValue={30}
                                    min={1}
                                    max={999999}
                                    sx={{ width: "10em" }}
                                    validate={validate_0_999999}
                                />
                                <TextInputWide
                                    source="repository_branch_housekeeping_exempt_branches"
                                    label="Exempt branches / versions"
                                    helperText="Regular expression which branches / version to exempt from deletion"
                                    validate={validate_255}
                                />
                            </Fragment>
                        )
                    }
                </FormDataConsumer>
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Notifications
            </Typography>
            <Stack spacing={2}>
                <TextInputWide
                    source="notification_email_to"
                    label="Email"
                    helperText="Comma separated email to addresses"
                    validate={validate_255}
                />
                <TextInputWide
                    source="notification_ms_teams_webhook"
                    label="MS Teams"
                    helperText="Webhook URL to send notifications to MS Teams"
                    validate={validate_255}
                />
                <TextInputWide
                    source="notification_slack_webhook"
                    label="Slack"
                    helperText="Webhook URL to send notifications to Slack"
                    validate={validate_255}
                />
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                Security Gate
            </Typography>
            <NullableBooleanInput
                source="security_gate_active"
                defaultValue={null}
                nullLabel="Standard"
                falseLabel="Disabled"
                trueLabel="Product specific"
                label="Security gate"
                helperText="Shows that the product does not exceed a defined amount of vulnerabilities per severity"
            />
            <FormDataConsumer>
                {({ formData }) =>
                    formData.security_gate_active && (
                        <Stack spacing={1}>
                            <NumberInput
                                label="Threshold critical"
                                source="security_gate_threshold_critical"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                            <NumberInput
                                label="Threshold high"
                                source="security_gate_threshold_high"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                            <NumberInput
                                label="Threshold medium"
                                source="security_gate_threshold_medium"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                            <NumberInput
                                label="Threshold low"
                                source="security_gate_threshold_low"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                            <NumberInput
                                label="Threshold none"
                                source="security_gate_threshold_none"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                            <NumberInput
                                label="Threshold unknown"
                                source="security_gate_threshold_unknown"
                                min={0}
                                max={999999}
                                sx={{ width: "12em" }}
                                validate={validate_0_999999}
                            />
                        </Stack>
                    )
                }
            </FormDataConsumer>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Issue Tracker
            </Typography>
            <BooleanInput
                source="issue_tracker_active"
                label="Active"
                defaultValue={false}
                helperText="Send observations to an issue tracker"
                sx={{ marginBottom: 2 }}
            />
            <AutocompleteInputMedium source="issue_tracker_type" label="Type" choices={ISSUE_TRACKER_TYPE_CHOICES} />
            <FormDataConsumer>
                {({ formData }) =>
                    formData.issue_tracker_type && (
                        <Stack spacing={1}>
                            <TextInputWide source="issue_tracker_base_url" label="Base URL" validate={validate_255} />
                            <TextInputWide source="issue_tracker_api_key" label="API key" validate={validate_255} />
                            <TextInputWide
                                source="issue_tracker_project_id"
                                label="Project id"
                                validate={validate_255}
                            />
                            <TextInputWide source="issue_tracker_labels" label="Labels" validate={validate_255} />
                            <AutocompleteInputMedium
                                source="issue_tracker_minimum_severity"
                                label="Minimum severity"
                                choices={OBSERVATION_SEVERITY_CHOICES}
                            />
                            <FormDataConsumer>
                                {({ formData }) =>
                                    formData.issue_tracker_type == "Jira" && (
                                        <Stack spacing={1}>
                                            <TextInputWide
                                                source="issue_tracker_username"
                                                label="Username (only for Jira)"
                                                validate={validate_255}
                                            />
                                            <TextInputWide
                                                source="issue_tracker_issue_type"
                                                label="Issue type (only for Jira)"
                                                validate={validate_255}
                                            />
                                            <TextInputWide
                                                source="issue_tracker_status_closed"
                                                label="Closed status (only for Jira)"
                                                validate={validate_255}
                                            />
                                        </Stack>
                                    )
                                }
                            </FormDataConsumer>
                        </Stack>
                    )
                }
            </FormDataConsumer>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Review
            </Typography>
            <BooleanInput source="assessments_need_approval" label="Assessments need approval" defaultValue={false} />
            <BooleanInput source="product_rules_need_approval" label="Rules need approval" defaultValue={false} />
            <BooleanInput
                source="new_observations_in_review"
                label='Status "In review" for new observations'
                defaultValue={false}
            />

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Risk acceptance expiry
            </Typography>
            <Stack direction="row" spacing={4}>
                <NullableBooleanInput
                    source="risk_acceptance_expiry_active"
                    label="Risk acceptance expiry"
                    defaultValue={null}
                    nullLabel="Standard"
                    falseLabel="Disabled"
                    trueLabel="Product specific"
                    helperText="Set date for expiry or risk acceptance"
                    sx={{ width: "15em", marginBottom: 2 }}
                />
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.risk_acceptance_expiry_active && (
                            <NumberInput
                                source="risk_acceptance_expiry_days"
                                label="Risk acceptance expiry (days)"
                                helperText="Days after which the risk acceptance expires"
                                defaultValue={30}
                                min={1}
                                max={999999}
                                validate={validate_0_999999}
                            />
                        )
                    }
                </FormDataConsumer>
            </Stack>

            {feature_license_management() && (
                <Fragment>
                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        License management
                    </Typography>
                    <ReferenceInput
                        source="license_policy"
                        reference="license_policies"
                        label="License policy"
                        sort={{ field: "name", order: "ASC" }}
                    >
                        <AutocompleteInputWide optionText="name" />
                    </ReferenceInput>
                </Fragment>
            )}

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Vulnerability scanning
            </Typography>

            <Stack direction="row" spacing={2} alignItems="center">
                <BooleanInput source="osv_enabled" label="OSV scanning enabled" defaultValue={false} />
                <FormDataConsumer>
                    {({ formData }) => formData.osv_enabled && <OSVLinuxDistributionInput />}
                </FormDataConsumer>
            </Stack>
            <FormDataConsumer>
                {({ formData }) =>
                    formData.osv_enabled && (
                        <Fragment>
                            {feature_automatic_osv_scanning() && (
                                <BooleanInput
                                    source="automatic_osv_scanning_enabled"
                                    label="Automatic OSV scanning enabled"
                                    defaultValue={false}
                                />
                            )}
                        </Fragment>
                    )
                }
            </FormDataConsumer>
        </Fragment>
    );
};
