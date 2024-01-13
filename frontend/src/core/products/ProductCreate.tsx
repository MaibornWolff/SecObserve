import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    BooleanInput,
    Create,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    ReferenceInput,
    SimpleForm,
    required,
} from "react-admin";

import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { ISSUE_TRACKER_TYPE_CHOICES } from "../types";

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
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6">Product</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />
                <ReferenceInput
                    source="product_group"
                    reference="product_groups"
                    sort={{ field: "name", order: "ASC" }}
                >
                    <AutocompleteInputWide optionText="name" />
                </ReferenceInput>

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Rules
                </Typography>
                <BooleanInput source="apply_general_rules" defaultValue={true} />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Source code repository
                </Typography>
                <TextInputWide
                    source="repository_prefix"
                    helperText="URL prefix to link to a file in the source code repository"
                />
                <NullableBooleanInput
                    source="repository_branch_housekeeping_active"
                    label="Housekeeping"
                    defaultValue={null}
                    nullLabel="Standard"
                    falseLabel="Disabled"
                    trueLabel="Product specific"
                    helperText="Delete inactive branches"
                    sx={{ width: "15em" }}
                />
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.repository_branch_housekeeping_active && (
                            <div>
                                <NumberInput
                                    source="repository_branch_housekeeping_keep_inactive_days"
                                    label="Keep inactive"
                                    helperText="Days before incative branches and their observations are deleted"
                                    defaultValue={30}
                                    min={1}
                                    max={999999}
                                />
                                <br />
                                <TextInputWide
                                    source="repository_branch_housekeeping_exempt_branches"
                                    label="Exempt branches"
                                    helperText="Regular expression which branches to exempt from deletion"
                                />
                                <br />
                            </div>
                        )
                    }
                </FormDataConsumer>

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Notifications
                </Typography>
                <TextInputWide
                    source="notification_email_to"
                    label="Email"
                    helperText="Comma separated email to addresses to send notifications via email"
                />
                <TextInputWide
                    source="notification_ms_teams_webhook"
                    label="MS Teams"
                    helperText="Webhook URL to send notifications to MS Teams"
                />
                <TextInputWide
                    source="notification_slack_webhook"
                    label="Slack"
                    helperText="Webhook URL to send notifications to Slack"
                />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
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
                            <div>
                                <NumberInput
                                    label="Threshold critical"
                                    source="security_gate_threshold_critical"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                                <NumberInput
                                    label="Threshold high"
                                    source="security_gate_threshold_high"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                                <NumberInput
                                    label="Threshold medium"
                                    source="security_gate_threshold_medium"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                                <NumberInput
                                    label="Threshold low"
                                    source="security_gate_threshold_low"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                                <NumberInput
                                    label="Threshold none"
                                    source="security_gate_threshold_none"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                                <NumberInput
                                    label="Threshold unkown"
                                    source="security_gate_threshold_unkown"
                                    min={0}
                                    max={999999}
                                />
                                <br />
                            </div>
                        )
                    }
                </FormDataConsumer>
                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Issue Tracker
                </Typography>
                <BooleanInput
                    source="issue_tracker_active"
                    label="Active"
                    defaultValue={false}
                    helperText="Send observations to an issue tracker"
                />
                <AutocompleteInputMedium
                    source="issue_tracker_type"
                    label="Type"
                    choices={ISSUE_TRACKER_TYPE_CHOICES}
                />
                <FormDataConsumer>
                    {({ formData }) =>
                        formData.issue_tracker_type && (
                            <div>
                                <TextInputWide source="issue_tracker_base_url" label="Base URL" />
                                <br />
                                <TextInputWide source="issue_tracker_api_key" label="API key" />
                                <br />
                                <TextInputWide source="issue_tracker_project_id" label="Project id" />
                                <br />
                                <TextInputWide source="issue_tracker_labels" label="Labels" />
                                <br />
                                <FormDataConsumer>
                                    {({ formData }) =>
                                        formData.issue_tracker_type == "Jira" && (
                                            <div>
                                                <TextInputWide
                                                    source="issue_tracker_username"
                                                    label="Username (only for Jira)"
                                                />
                                                <br />
                                                <TextInputWide
                                                    source="issue_tracker_issue_type"
                                                    label="Issue type (only for Jira)"
                                                />
                                                <br />
                                                <TextInputWide
                                                    source="issue_tracker_status_closed"
                                                    label="Closed status (only for Jira)"
                                                />
                                                <br />
                                            </div>
                                        )
                                    }
                                </FormDataConsumer>
                            </div>
                        )
                    }
                </FormDataConsumer>
            </SimpleForm>
        </Create>
    );
};

const requiredValidate = [required()];

export default ProductCreate;
