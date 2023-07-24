import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    BooleanInput,
    DeleteButton,
    Edit,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    WithRecord,
    required,
    useRecordContext,
} from "react-admin";

import { PERMISSION_PRODUCT_DELETE } from "../../access_control/types";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { ISSUE_TRACKER_TYPE_CHOICES } from "../types";

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

const ProductEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        if (!data.repository_prefix) {
            data.repository_prefix = "";
        }
        if (!data.notification_email_to) {
            data.notification_email_to = "";
        }
        if (!data.notification_ms_teams_webhook) {
            data.notification_ms_teams_webhook = "";
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
        if (!data.issue_tracker_status_closed) {
            data.issue_tracker_status_closed = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
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
                <BooleanInput source="apply_general_rules" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Source code repository
                </Typography>
                <TextInputWide source="repository_prefix" />
                <WithRecord
                    render={(product) => (
                        <ReferenceInput
                            source="repository_default_branch"
                            reference="branches"
                            label="Default branch"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ product: product.id }}
                        >
                            <AutocompleteInputWide optionText="name" />
                        </ReferenceInput>
                    )}
                />
                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Notifications
                </Typography>
                <TextInputWide
                    source="notification_email_to"
                    label="Email"
                    helperText="Comma separated email to addresses"
                />
                <TextInputWide source="notification_ms_teams_webhook" label="MS Teams" helperText="Webhook URL" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Security Gate
                </Typography>
                <NullableBooleanInput source="security_gate_active" defaultValue={null} />
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
                <BooleanInput source="issue_tracker_active" label="Active" />
                <AutocompleteInputMedium
                    source="issue_tracker_type"
                    label="Type"
                    choices={ISSUE_TRACKER_TYPE_CHOICES}
                />
                <TextInputWide source="issue_tracker_base_url" label="Base URL" />
                <TextInputWide source="issue_tracker_api_key" label="API key" inputProps={{ autocomplete: "off" }} />
                <TextInputWide source="issue_tracker_project_id" label="Project id" />
                <TextInputWide source="issue_tracker_labels" label="Labels" />
                <TextInputWide source="issue_tracker_username" label="Username (only for Jira)" />
                <TextInputWide source="issue_tracker_status_closed" label="Closed status (only for Jira)" />
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ProductEdit;
