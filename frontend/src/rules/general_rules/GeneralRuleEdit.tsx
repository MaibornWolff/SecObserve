import { useState } from "react";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, WithRecord } from "react-admin";

import { RuleEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton alwaysEnable />
            <DeleteButton mutationMode="pessimistic" />
        </Toolbar>
    );
};

const GeneralRuleEdit = () => {
    const [description, setDescription] = useState("");

    const transform = (data: any) => {
        return non_duplicate_transform(data, description);
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />} validate={validateRuleForm}>
                <WithRecord
                    render={(general_rule) => (
                        <RuleEditComponent
                            product={null}
                            initialStatus={general_rule ? general_rule.new_status : ""}
                            setDescription={setDescription}
                        />
                    )}
                />
            </SimpleForm>
        </Edit>
    );
};

export default GeneralRuleEdit;
