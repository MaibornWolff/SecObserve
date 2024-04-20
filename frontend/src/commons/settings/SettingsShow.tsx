import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    DateField,
    Labeled,
    NumberField,
    ReferenceField,
    Show,
    TextField,
    WithRecord,
} from "react-admin";

import settings from ".";
import ListHeader from "../../commons/layout/ListHeader";

const SettingsShowComponent = () => {
    return (
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
                </Stack>
            </Paper>

            <Paper sx={{ marginBottom: 2, padding: 2 }}>
                <Typography variant="h6">Background tasks (restart needed)</Typography>
                <Stack spacing={2}>
                    <Labeled label="Product metrics interval (minutes)">
                        <NumberField source="background_product_metrics_interval_minutes" />
                    </Labeled>
                    <Labeled label="EPSS import crontab (hours)">
                        <NumberField source="background_epss_import_crontab_hours" />
                    </Labeled>
                    <Labeled label="EPSS import crontab (minutes)">
                        <NumberField source="background_epss_import_crontab_minutes" />
                    </Labeled>
                </Stack>
            </Paper>

            <Paper sx={{ marginBottom: 2, padding: 2 }}>
                <Typography variant="h6">Features</Typography>
                <Stack spacing={2}>
                    <Labeled label="VEX">
                        <BooleanField source="feature_vex" />
                    </Labeled>
                </Stack>
            </Paper>

            <Paper sx={{ marginBottom: 2, padding: 2 }}>
                <Typography variant="h6">Housekeeping for branches</Typography>
                <Stack spacing={2}>
                    <Labeled label="Branch housekeeping crontab (hours)">
                        <NumberField source="branch_housekeeping_crontab_hours" />
                    </Labeled>
                    <Labeled label="Branch housekeeping crontab (minutes)">
                        <NumberField source="branch_housekeeping_crontab_minutes" />
                    </Labeled>
                    <Labeled label="Branch housekeeping active">
                        <BooleanField source="branch_housekeeping_active" />
                    </Labeled>
                    <Labeled label="Branch housekeeping keep inactive (days)">
                        <NumberField source="branch_housekeeping_keep_inactive_days" />
                    </Labeled>
                    <Labeled label="Branch housekeeping exempt branches">
                        <TextField source="branch_housekeeping_exempt_branches" />
                    </Labeled>
                </Stack>
            </Paper>

            <Paper sx={{ marginBottom: 2, padding: 2 }}>
                <Typography variant="h6">Integrations</Typography>
                <Stack spacing={2}>
                    <Labeled label="Base URL frontend">
                        <TextField source="base_url_frontend" />
                    </Labeled>
                    <Labeled label="Email from">
                        <TextField source="email_from" />
                    </Labeled>
                    <Labeled label="Exception email to">
                        <TextField source="exception_email_to" />
                    </Labeled>
                    <Labeled label="Exception MS Teams webhook">
                        <TextField source="exception_ms_teams_webhook" />
                    </Labeled>
                    <Labeled label="Exception Slack webhook">
                        <TextField source="exception_slack_webhook" />
                    </Labeled>
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
                    <Labeled label="Threshold unkown">
                        <NumberField source="security_gate_threshold_unkown" />
                    </Labeled>
                </Stack>
            </Paper>
        </Box>
    );
};
const SettingsShow = () => {
    return (
        <Fragment>
            <ListHeader icon={settings.icon} title="Settings" />
            <Show component={SettingsShowComponent}>
                <Fragment />
            </Show>
        </Fragment>
    );
};

export default SettingsShow;
