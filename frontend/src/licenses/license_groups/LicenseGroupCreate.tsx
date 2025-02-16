import { Typography } from "@mui/material";
import { BooleanInput, Create, SimpleForm } from "react-admin";

import license_groups from ".";
import { validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const LicenseGroupCreate = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                    <license_groups.icon />
                    &nbsp;&nbsp;License Group
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <TextInputWide
                    source="description"
                    multiline
                    minRows={3}
                    validate={validate_2048}
                    helperText="Markdown supported."
                />
                <BooleanInput source="is_public" label="Public" />
            </SimpleForm>
        </Create>
    );
};

export default LicenseGroupCreate;
