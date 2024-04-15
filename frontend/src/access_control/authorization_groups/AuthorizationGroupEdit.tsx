import { Typography } from "@mui/material";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar } from "react-admin";

import { validate_255, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" redirect="/access_control/authorization_groups" />
        </Toolbar>
    );
};

const AuthorizationGroupEdit = () => {
    const transform = (data: any) => {
        if (!data.oidc_group) {
            data.oidc_group = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Authorization Group
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <TextInputWide source="oidc_group" label="OIDC group" validate={validate_255} />
            </SimpleForm>
        </Edit>
    );
};

export default AuthorizationGroupEdit;
