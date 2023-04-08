import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import {
    BooleanInput,
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

const ProductEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        if (!data.repository_prefix) {
            data.repository_prefix = "";
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
                <Typography variant="h6">Product</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Rules
                </Typography>
                <BooleanInput source="apply_general_rules" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Integrations
                </Typography>
                <TextInputWide source="repository_prefix" />
                <TextInputWide source="ms_teams_webhook" label="MS Teams Webhook" />

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
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ProductEdit;
