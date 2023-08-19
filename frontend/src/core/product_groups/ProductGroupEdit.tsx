import { Typography } from "@mui/material";
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
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6">Product Group</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />

                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Source code repository
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
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ProductGroupEdit;
