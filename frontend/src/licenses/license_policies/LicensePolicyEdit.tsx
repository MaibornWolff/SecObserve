import { Typography } from "@mui/material";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar } from "react-admin";

import { validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" redirect="/license/license_policies" />
        </Toolbar>
    );
};

const LicensePolicyEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    License Policy
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <TextInputWide
                    source="description"
                    multiline
                    minRows={3}
                    validate={validate_2048}
                    helperText="Markdown supported."
                />
            </SimpleForm>
        </Edit>
    );
};

export default LicensePolicyEdit;
