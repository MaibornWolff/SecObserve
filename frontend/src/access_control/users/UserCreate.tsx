import { Divider, Typography } from "@mui/material";
import { BooleanInput, Create, SimpleForm } from "react-admin";

import { validate_150, validate_255, validate_required_150 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const UserCreate = () => {
    const transform = (data: any) => {
        if (!data.full_name) {
            data.full_name = "";
        }
        if (!data.first_name) {
            data.first_name = "";
        }
        if (!data.last_name) {
            data.last_name = "";
        }
        if (!data.email) {
            data.email = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    User
                </Typography>
                <TextInputWide autoFocus source="username" validate={validate_required_150} />
                <TextInputWide source="full_name" validate={validate_255} />
                <TextInputWide source="first_name" validate={validate_150} />
                <TextInputWide source="last_name" validate={validate_150} />
                <TextInputWide source="email" validate={validate_255} />

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Permissions
                </Typography>
                <BooleanInput source="is_active" label="Active" defaultValue={true} />
                <BooleanInput source="is_external" label="External" />
                <BooleanInput source="is_superuser" label="Superuser" />
            </SimpleForm>
        </Create>
    );
};

export default UserCreate;
