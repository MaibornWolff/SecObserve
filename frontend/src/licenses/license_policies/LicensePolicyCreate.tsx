import { Typography } from "@mui/material";
import { BooleanInput, Create, ReferenceInput, SimpleForm } from "react-admin";

import license_policies from ".";
import { validate_255, validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";

const LicensePolicyCreate = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        if (!data.ignore_component_types) {
            data.ignore_component_types = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                    <license_policies.icon />
                    &nbsp;&nbsp;License Policy
                </Typography>
                <TextInputWide autoFocus source="name" validate={validate_required_255} />
                <TextInputWide
                    source="description"
                    multiline
                    minRows={3}
                    validate={validate_2048}
                    helperText="Markdown supported."
                />
                <ReferenceInput
                    source="parent"
                    reference="license_policies"
                    filter={{ is_child: false }}
                    sort={{ field: "name", order: "ASC" }}
                >
                    <AutocompleteInputWide optionText="name" />
                </ReferenceInput>
                <TextInputWide source="ignore_component_types" validate={validate_255} />
                <BooleanInput source="is_public" label="Public" />
            </SimpleForm>
        </Create>
    );
};

export default LicensePolicyCreate;
