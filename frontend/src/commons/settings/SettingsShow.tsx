import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { BooleanField, EditButton, Labeled, NumberField, Show, TextField, TopToolbar, WithRecord } from "react-admin";

import settings from ".";
import ListHeader from "../../commons/layout/ListHeader";
import JWTSecretReset from "./JWTSecretReset";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <JWTSecretReset />
                <EditButton />
            </Stack>
        </TopToolbar>
    );
};

const SettingsShowComponent = () => {
    return (
        <WithRecord
            render={(settings) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Authentication</Typography>
                        <Stack spacing={2}>
                            <Labeled label="JWT validity duration user (hours)">
                                <NumberField source="jwt_validity_duration_user" />
                            </Labeled>
                            <Labeled label="JWT validity duration superuser (hours)">
                                <NumberField source="jwt_validity_duration_superuser" />
                            </Labeled>
                            {settings.internal_users && (
                                <Labeled label="Internal users">
                                    <TextField source="internal_users" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Background tasks (restart needed)</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Product metrics interval (minutes)">
                                <NumberField source="background_product_metrics_interval_minutes" />
                            </Labeled>
                            <Stack direction="row" spacing={2}>
                                <Labeled label="EPSS import crontab (hour/UTC)">
                                    <NumberField source="background_epss_import_crontab_hour" />
                                </Labeled>
                                <Labeled label="EPSS import crontab (minutes)">
                                    <NumberField source="background_epss_import_crontab_minute" />
                                </Labeled>
                            </Stack>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Features</Typography>
                        <Stack spacing={2}>
                            <Labeled label="VEX">
                                <BooleanField source="feature_vex" />
                            </Labeled>
                            <Labeled label="Disable user login">
                                <BooleanField source="feature_disable_user_login" />
                            </Labeled>
                            <Labeled label="General rules need approval">
                                <BooleanField source="feature_general_rules_need_approval" />
                            </Labeled>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Housekeeping for branches</Typography>
                        <Stack spacing={2}>
                            <Stack direction="row" spacing={2}>
                                <Labeled label="Branch housekeeping crontab (hour/UTC)">
                                    <NumberField source="branch_housekeeping_crontab_hour" />
                                </Labeled>
                                <Labeled label="Branch housekeeping crontab (minute)">
                                    <NumberField source="branch_housekeeping_crontab_minute" />
                                </Labeled>
                            </Stack>
                            <Labeled label="Branch housekeeping active">
                                <BooleanField source="branch_housekeeping_active" />
                            </Labeled>
                            <Labeled label="Branch housekeeping keep inactive (days)">
                                <NumberField source="branch_housekeeping_keep_inactive_days" />
                            </Labeled>
                            {settings.branch_housekeeping_exempt_branches && (
                                <Labeled label="Branch housekeeping exempt branches">
                                    <TextField source="branch_housekeeping_exempt_branches" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Integrations</Typography>
                        <Stack spacing={2}>
                            {settings.base_url_frontend && (
                                <Labeled label="Base URL frontend">
                                    <TextField source="base_url_frontend" />
                                </Labeled>
                            )}
                            {settings.email_from && (
                                <Labeled label="Email from">
                                    <TextField source="email_from" />
                                </Labeled>
                            )}
                            {settings.exception_email_to && (
                                <Labeled label="Exception email to">
                                    <TextField source="exception_email_to" />
                                </Labeled>
                            )}
                            {settings.exception_ms_teams_webhook && (
                                <Labeled label="Exception MS Teams webhook">
                                    <TextField source="exception_ms_teams_webhook" />
                                </Labeled>
                            )}
                            {settings.exception_slack_webhook && (
                                <Labeled label="Exception Slack webhook">
                                    <TextField source="exception_slack_webhook" />
                                </Labeled>
                            )}
                            <Labeled label="Exception rate limit">
                                <NumberField source="exception_rate_limit" />
                            </Labeled>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Security gates</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Security gates active">
                                <BooleanField source="security_gate_active" />
                            </Labeled>
                            {settings.security_gate_active && (
                                <Fragment>
                                    <Labeled label="Threshold critical">
                                        <NumberField source="security_gate_threshold_critical" />
                                    </Labeled>
                                    <Labeled label="Threshold high">
                                        <NumberField source="security_gate_threshold_high" />
                                    </Labeled>
                                    <Labeled label="Threshold medium">
                                        <NumberField source="security_gate_threshold_medium" />
                                    </Labeled>
                                    <Labeled label="Threshold low">
                                        <NumberField source="security_gate_threshold_low" />
                                    </Labeled>
                                    <Labeled label="Threshold none">
                                        <NumberField source="security_gate_threshold_none" />
                                    </Labeled>
                                    <Labeled label="Threshold unknown">
                                        <NumberField source="security_gate_threshold_unknown" />
                                    </Labeled>
                                </Fragment>
                            )}
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Risk acceptance expiry</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Risk acceptance expiry (days)">
                                <NumberField source="risk_acceptance_expiry_days" />
                            </Labeled>
                            <Stack direction="row" spacing={2}>
                                <Labeled label="Risk acceptance expiry crontab (hour/UTC)">
                                    <NumberField source="risk_acceptance_expiry_crontab_hour" />
                                </Labeled>
                                <Labeled label="Risk acceptance expiry crontab (minute)">
                                    <NumberField source="risk_acceptance_expiry_crontab_minute" />
                                </Labeled>
                            </Stack>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Automatic API import</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Enable automatic API imports">
                                <BooleanField source="feature_automatic_api_import" />
                            </Labeled>
                            {settings.feature_automatic_api_import && (
                                <Stack direction="row" spacing={2}>
                                    <Labeled label="API import crontab (hour/UTC)">
                                        <NumberField source="api_import_crontab_hour" />
                                    </Labeled>
                                    <Labeled label="API import crontab (minute)">
                                        <NumberField source="api_import_crontab_minute" />
                                    </Labeled>
                                </Stack>
                            )}
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Password validation for non-OIDC users</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Minimum length">
                                <NumberField source="password_validator_minimum_length" />
                            </Labeled>
                            <Labeled label="Attribute similarity">
                                <BooleanField source="password_validator_attribute_similarity" />
                            </Labeled>
                            <Labeled label="Common passwords">
                                <BooleanField source="password_validator_common_passwords" />
                            </Labeled>
                            <Labeled label="Not entirely numeric">
                                <BooleanField source="password_validator_not_numeric" />
                            </Labeled>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">License management</Typography>
                        <Stack spacing={2}>
                            <Labeled label="Enable license management">
                                <BooleanField source="feature_license_management" />
                            </Labeled>
                            {settings.feature_license_management && (
                                <Stack direction="row" spacing={2}>
                                    <Labeled label="License import crontab (hour/UTC)">
                                        <NumberField source="license_import_crontab_hour" />
                                    </Labeled>
                                    <Labeled label="License import crontab (minute)">
                                        <NumberField source="license_import_crontab_minute" />
                                    </Labeled>
                                </Stack>
                            )}
                        </Stack>
                    </Paper>
                </Box>
            )}
        />
    );
};
const SettingsShow = () => {
    return (
        <Fragment>
            <ListHeader icon={settings.icon} title="Settings" />
            <Show component={SettingsShowComponent} actions={<ShowActions />}>
                <Fragment />
            </Show>
        </Fragment>
    );
};

export default SettingsShow;
