import { Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanInput,
    DeleteButton,
    Edit,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    WithRecord,
} from "react-admin";

import { validate_255, validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";

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
        if (!data.ignore_component_types) {
            data.ignore_component_types = "";
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
                <WithRecord
                    render={(license_policy) => (
                        <Fragment>
                            {!license_policy.is_parent && (
                                <ReferenceInput
                                    source="parent"
                                    reference="license_policies"
                                    filter={{ is_child: false, is_not_id: license_policy.id }}
                                    sort={{ field: "name", order: "ASC" }}
                                >
                                    <AutocompleteInputWide optionText="name" />
                                </ReferenceInput>
                            )}
                        </Fragment>
                    )}
                />
                <TextInputWide source="ignore_component_types" validate={validate_255} />
                <BooleanInput source="is_public" label="Public" />
            </SimpleForm>
        </Edit>
    );
};

export default LicensePolicyEdit;
