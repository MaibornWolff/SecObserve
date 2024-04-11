import { Divider, Typography } from "@mui/material";
import { BooleanInput, DeleteButton, Edit, SaveButton, SimpleForm, Toolbar } from "react-admin";

import { validate_150, validate_255, validate_required_150 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" redirect="/access_control/users" />
        </Toolbar>
    );
};

const UserEdit = () => {
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
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    User
                </Typography>
                <TextInputWide autoFocus source="username" validate={validate_required_150} />
                <TextInputWide source="full_name" validate={validate_255} />
                <TextInputWide source="first_name" validate={validate_150} />
                <TextInputWide source="last_name" validate={validate_150} />
                <TextInputWide source="email" validate={validate_255} />
                <BooleanInput source="is_oidc_user" label="OIDC user" readOnly />

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Permissions
                </Typography>
                <BooleanInput source="is_active" label="Active" />
                <BooleanInput source="is_external" label="External" />
                <BooleanInput source="is_superuser" label="Superuser" />
            </SimpleForm>
        </Edit>
    );
};

export default UserEdit;
