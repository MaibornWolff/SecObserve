import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    BooleanInput,
    Create,
    FormDataConsumer,
    NullableBooleanInput,
    NumberInput,
    SimpleForm,
    required,
} from "react-admin";

import { AutocompleteInputMedium, PasswordInputWide, TextInputWide } from "../../commons/layout/themes";
import { ISSUE_TRACKER_TYPE_CHOICES } from "../types";

const ProductCreate = () => {
    return (
        <Create redirect="show">
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6">Product</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Rules
                </Typography>
                <BooleanInput source="apply_general_rules" defaultValue={true} />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Source code repository
                </Typography>
                <TextInputWide source="repository_prefix" />
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
                    Issue Tracker (Experimental)
                </Typography>
                <BooleanInput source="issue_tracker_active" label="Active" defaultValue={false} />
                <AutocompleteInputMedium
                    source="issue_tracker_type"
                    label="Type"
                    choices={ISSUE_TRACKER_TYPE_CHOICES}
                />
                <TextInputWide source="issue_tracker_base_url" label="Base URL" />
                <PasswordInputWide
                    source="issue_tracker_api_key"
                    label="API key"
                    inputProps={{ autocomplete: "current-password" }}
                />
                <TextInputWide source="issue_tracker_project_id" label="Project id" />
                <TextInputWide source="issue_tracker_labels" label="Labels" />
            </SimpleForm>
        </Create>
    );
};

const requiredValidate = [required()];

export default ProductCreate;
