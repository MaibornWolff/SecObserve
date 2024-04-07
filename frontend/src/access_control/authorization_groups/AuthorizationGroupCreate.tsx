import { Typography } from "@mui/material";
import { Create, SimpleForm } from "react-admin";

import { validate_255, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const AuthorizationGroupCreate = () => {
    const transform = (data: any) => {
        if (!data.oidc_group) {
            data.oidc_group = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Authorization Group
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <TextInputWide source="oidc_group" label="OIDC group" validate={validate_255} />
            </SimpleForm>
        </Create>
    );
};

export default AuthorizationGroupCreate;
