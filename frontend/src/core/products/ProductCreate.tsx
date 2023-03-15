import {
    Create,
    SimpleForm,
    required,
    NullableBooleanInput,
    NumberInput,
    FormDataConsumer,
    BooleanInput,
} from "react-admin";
import { RichTextInput } from "ra-input-rich-text";

import { Typography } from "@mui/material";

import { TextInputWide } from "../../commons/layout/themes";

const ProductCreate = () => {
    return (
        <Create redirect="show">
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6">Product</Typography>
                <TextInputWide
                    autoFocus
                    source="name"
                    validate={requiredValidate}
                />
                <RichTextInput source="description" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Rules
                </Typography>
                <BooleanInput
                    source="apply_general_rules"
                    defaultValue={true}
                />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Integrations
                </Typography>
                <TextInputWide source="repository_prefix" />
                <TextInputWide
                    source="ms_teams_webhook"
                    label="MS Teams Webhook"
                />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Security Gate
                </Typography>
                <NullableBooleanInput
                    source="security_gate_active"
                    defaultValue={null}
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
        </Create>
    );
};

const requiredValidate = [required()];

export default ProductCreate;
