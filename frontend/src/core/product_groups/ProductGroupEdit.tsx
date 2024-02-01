import { Divider, Stack, Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    DeleteButton,
    Edit,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useRecordContext,
} from "react-admin";

import { PERMISSION_PRODUCT_DELETE } from "../../access_control/types";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    const product = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            {product && product.permissions.includes(PERMISSION_PRODUCT_DELETE) && (
                <DeleteButton mutationMode="pessimistic" />
            )}
        </Toolbar>
    );
};

const ProductGroupEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
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
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Product Group
                </Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Housekeeping (for products)
                </Typography>
                <NullableBooleanInput
                    source="repository_branch_housekeeping_active"
                    label="Housekeeping"
                    defaultValue={null}
                    nullLabel="Standard"
                    falseLabel="Disabled"
                    trueLabel="Product group specific"
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

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Notifications (for products)
                </Typography>
                <Stack spacing={2}>
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
                </Stack>

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Security Gate (for products)
                </Typography>
                <NullableBooleanInput
                    source="security_gate_active"
                    defaultValue={null}
                    nullLabel="Standard"
                    falseLabel="Disabled"
                    trueLabel="Product group specific"
                    label="Security gate"
                    helperText="Shows that a product does not exceed a defined amount of vulnerabilities per severity"
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
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ProductGroupEdit;
