import { Divider, Typography } from "@mui/material";
import { Fragment } from "react";
import { BooleanInput, Edit, NumberInput, SaveButton, SimpleForm, Toolbar } from "react-admin";

import settings from ".";
import { validate_0_23, validate_0_59, validate_0_999999, validate_255 } from "../../commons/custom_validators";
import ListHeader from "../../commons/layout/ListHeader";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
        </Toolbar>
    );
};

const SettingsEdit = () => {
    const transform = (data: any) => {
        if (!data.branch_housekeeping_exempt_branches) {
            data.branch_housekeeping_exempt_branches = "";
        }
        if (!data.base_url_frontend) {
            data.base_url_frontend = "";
        }
        if (!data.email_from) {
            data.email_from = "";
        }
        if (!data.exception_email_to) {
            data.exception_email_to = "";
        }
        if (!data.exception_ms_teams_webhook) {
            data.exception_ms_teams_webhook = "";
        }
        if (!data.exception_slack_webhook) {
            data.exception_slack_webhook = "";
        }
        return data;
    };

    return (
        <Fragment>
            <ListHeader icon={settings.icon} title="Settings" />
            <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
                <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Authentication
                    </Typography>
                    <NumberInput
                        autoFocus
                        source="jwt_validity_duration_user"
                        label="JWT validity duration user (hours)"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Validity duration of JWT tokens for regular users in hours"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="jwt_validity_duration_superuser"
                        label="JWT validity duration superuser (hours)"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Validity duration of JWT tokens for superusers in hours"
                        sx={{ marginBottom: 2 }}
                    />

                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Background tasks (restart needed)
                    </Typography>
                    <NumberInput
                        source="background_product_metrics_interval_minutes"
                        label="Product metrics interval (minutes)"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Calculate product metrics every x minutes"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="background_epss_import_crontab_hours"
                        label="EPSS import crontab (hours)"
                        min={0}
                        step={1}
                        validate={validate_0_23}
                        helperText="Hours crontab expression for EPSS import (UTC)"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="background_epss_import_crontab_minutes"
                        label="EPSS import crontab (minutes)"
                        min={0}
                        step={1}
                        validate={validate_0_59}
                        helperText="Minutes crontab expression for EPSS import"
                        sx={{ marginBottom: 2 }}
                    />

                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Features
                    </Typography>
                    <BooleanInput
                        source="feature_vex"
                        label="VEX"
                        helperText="Generate VEX documents in OpenVEX and CSAF format"
                    />
                    <BooleanInput
                        source="feature_disable_user_login"
                        label="Disable user login"
                        helperText="Do not show user and password fields if OIDC login is enabled"
                        sx={{ marginBottom: 2 }}
                    />

                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Housekeeping for branches
                    </Typography>
                    <NumberInput
                        source="branch_housekeeping_crontab_hours"
                        label="Branch housekeeping crontab (hours)"
                        min={0}
                        step={1}
                        validate={validate_0_23}
                        helperText="Hours crontab expression for branch housekeeping (UTC)"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="branch_housekeeping_crontab_minutes"
                        label="Branch housekeeping crontab (minutes)"
                        min={0}
                        step={1}
                        validate={validate_0_59}
                        helperText="Minutes crontab expression for branch housekeeping"
                        sx={{ marginBottom: 2 }}
                    />
                    <BooleanInput
                        source="branch_housekeeping_active"
                        label="Branch housekeeping active"
                        helperText="Delete inactive branches"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="branch_housekeeping_keep_inactive_days"
                        label="Branch housekeeping keep inactive (days)"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Days before incative branches and their observations are deleted"
                        sx={{ marginBottom: 2 }}
                    />
                    <TextInputWide
                        source="branch_housekeeping_exempt_branches"
                        label="Branch housekeeping exempt branches"
                        validate={validate_255}
                        helperText="Regular expression which branches to exempt from deletion"
                        sx={{ marginBottom: 2 }}
                    />

                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Integrations
                    </Typography>
                    <TextInputWide
                        source="base_url_frontend"
                        label="Base URL frontend"
                        validate={validate_255}
                        helperText="Base URL of the frontend, used to set links in notifications correctly"
                        sx={{ marginBottom: 2 }}
                    />
                    <TextInputWide
                        source="email_from"
                        label="Email from"
                        validate={validate_255}
                        helperText="From address for sending email notifications"
                        sx={{ marginBottom: 2 }}
                    />
                    <TextInputWide
                        source="exception_email_to"
                        label="Exception email to"
                        validate={validate_255}
                        helperText="Comma separated email addresses to send exception notifications"
                        sx={{ marginBottom: 2 }}
                    />
                    <TextInputWide
                        source="exception_ms_teams_webhook"
                        label="Exception MS Teams webhook"
                        validate={validate_255}
                        helperText="MS Teams webhook to send exception notifications"
                        sx={{ marginBottom: 2 }}
                    />
                    <TextInputWide
                        source="exception_slack_webhook"
                        label="Exception Slack webhook"
                        validate={validate_255}
                        helperText="Slack webhook to send exception notifications"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="exception_rate_limit"
                        label="Exception rate limit"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Timedelta in seconds when to send the same exception the next time"
                        sx={{ marginBottom: 2 }}
                    />

                    <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6" sx={{ marginBottom: 2 }}>
                        Security gates
                    </Typography>
                    <BooleanInput
                        source="security_gate_active"
                        label="Security gates active"
                        helperText="Are security gates activated?"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_critical"
                        label="Threshold critical"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of critical observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_high"
                        label="Threshold high"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of high observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_medium"
                        label="Threshold medium"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of medium observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_low"
                        label="Threshold low"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of low observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_none"
                        label="Threshold none"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of none observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                    <NumberInput
                        source="security_gate_threshold_unkown"
                        label="Threshold unknown"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                        helperText="Number of unkown observations that must not be exceeded"
                        sx={{ marginBottom: 2 }}
                    />
                </SimpleForm>
            </Edit>
        </Fragment>
    );
};

export default SettingsEdit;
