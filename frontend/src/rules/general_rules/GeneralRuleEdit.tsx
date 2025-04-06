import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, WithRecord } from "react-admin";

import { RuleCreateEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" />
        </Toolbar>
    );
};

const GeneralRuleEdit = () => {
    const transform = (data: any) => {
        return non_duplicate_transform(data);
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />} validate={validateRuleForm}>
                <WithRecord
                    render={(general_rule) => (
                        <RuleCreateEditComponent
                            product={null}
                            initialStatus={general_rule ? general_rule.new_status : ""}
                        />
                    )}
                />
            </SimpleForm>
        </Edit>
    );
};

export default GeneralRuleEdit;
