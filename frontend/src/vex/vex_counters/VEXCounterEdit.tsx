import { Typography } from "@mui/material";
import { DeleteButton, Edit, NumberInput, SaveButton, SimpleForm, Toolbar } from "react-admin";

import { validate_0_999999, validate_2000_9999, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" />
        </Toolbar>
    );
};
const VEXCounterEdit = () => {
    return (
        <Edit redirect="show" mutationMode="pessimistic">
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    VEX Counter
                </Typography>
                <TextInputWide
                    autoFocus
                    source="document_id_prefix"
                    label="Document ID prefix"
                    validate={validate_required_255}
                />
                <NumberInput source="year" validate={validate_2000_9999} />
                <NumberInput source="counter" validate={validate_0_999999} />
            </SimpleForm>
        </Edit>
    );
};

export default VEXCounterEdit;
