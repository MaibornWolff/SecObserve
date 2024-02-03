import { Divider, Stack, Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    BooleanInput,
    Create,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    ReferenceInput,
    SimpleForm,
} from "react-admin";

import {
    validate_255,
    validate_2048,
    validate_min_0_999999,
    validate_required_255,
} from "../../commons/custom_validators";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { ISSUE_TRACKER_TYPE_CHOICES, OBSERVATION_SEVERITY_CHOICES } from "../types";

const ProductCreate = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
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
            if (data.security_gate_threshold_unkown == "") {
                data.security_gate_threshold_unkown = 0;
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
            if (data.security_gate_threshold_unkown == "") {
                data.security_gate_threshold_unkown = null;
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
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Product
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <RichTextInput source="description" validate={validate_2048} />
                <ReferenceInput
                    source="product_group"
                    reference="product_groups"
                    sort={{ field: "name", order: "ASC" }}
                >
                    <AutocompleteInputWide optionText="name" />
                </ReferenceInput>

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Rules
                </Typography>
                <BooleanInput source="apply_general_rules" defaultValue={true} />

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Source code repository
                </Typography>
                <Stack spacing={2} sx={{ marginBottom: 2 }}>
                    <TextInputWide
                        source="repository_prefix"
                        helperText="URL prefix to link to a file in the source code repository"
                        validate={validate_255}
                    />
                    <NullableBooleanInput
                        source="repository_branch_housekeeping_active"
                        label="Housekeeping"
                        defaultValue={null}
                        nullLabel="Standard"
                        falseLabel="Disabled"
                        trueLabel="Product specific"
                        helperText="Delete inactive branches"
                    />
                </Stack>
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.repository_branch_housekeeping_active && (
                            <Stack spacing={2}>
                                <NumberInput
                                    source="repository_branch_housekeeping_keep_inactive_days"
                                    label="Keep inactive"
                                    helperText="Days before incative branches and their observations are deleted"
                                    defaultValue={30}
                                    min={1}
                                    max={999999}
                                    validate={validate_min_0_999999}
                                />
                                <TextInputWide
                                    source="repository_branch_housekeeping_exempt_branches"
                                    label="Exempt branches"
                                    helperText="Regular expression which branches to exempt from deletion"
                                    validate={validate_255}
                                />
                            </Stack>
                        )
                    }
                </FormDataConsumer>

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Notifications
                </Typography>
                <Stack spacing={2}>
                    <TextInputWide
                        source="notification_email_to"
                        label="Email"
                        helperText="Comma separated email to addresses to send notifications via email"
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
                                    validate={validate_min_0_999999}
                                />
                                <NumberInput
                                    label="Threshold high"
                                    source="security_gate_threshold_high"
                                    min={0}
                                    max={999999}
                                    sx={{ width: "12em" }}
                                    validate={validate_min_0_999999}
                                />
                                <NumberInput
                                    label="Threshold medium"
                                    source="security_gate_threshold_medium"
                                    min={0}
                                    max={999999}
                                    sx={{ width: "12em" }}
                                    validate={validate_min_0_999999}
                                />
                                <NumberInput
                                    label="Threshold low"
                                    source="security_gate_threshold_low"
                                    min={0}
                                    max={999999}
                                    sx={{ width: "12em" }}
                                    validate={validate_min_0_999999}
                                />
                                <NumberInput
                                    label="Threshold none"
                                    source="security_gate_threshold_none"
                                    min={0}
                                    max={999999}
                                    sx={{ width: "12em" }}
                                    validate={validate_min_0_999999}
                                />
                                <NumberInput
                                    label="Threshold unkown"
                                    source="security_gate_threshold_unkown"
                                    min={0}
                                    max={999999}
                                    sx={{ width: "12em" }}
                                    validate={validate_min_0_999999}
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
                <AutocompleteInputMedium
                    source="issue_tracker_type"
                    label="Type"
                    choices={ISSUE_TRACKER_TYPE_CHOICES}
                />
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.issue_tracker_type && (
                            <Stack spacing={1}>
                                <TextInputWide
                                    source="issue_tracker_base_url"
                                    label="Base URL"
                                    validate={validate_255}
                                />
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
            </SimpleForm>
        </Create>
    );
};

export default ProductCreate;
