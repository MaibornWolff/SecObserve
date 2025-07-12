import { useState } from "react";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, WithRecord, useRecordContext } from "react-admin";

import { PERMISSION_PRODUCT_RULE_DELETE } from "../../access_control/types";
import { RuleEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const CustomToolbar = () => {
    const rule = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton alwaysEnable />
            {rule?.product_data.permissions.includes(PERMISSION_PRODUCT_RULE_DELETE) && (
                <DeleteButton
                    mutationMode="pessimistic"
                    redirect={"/products/" + rule.product_data.id + "/show/rules"}
                />
            )}
        </Toolbar>
    );
};
const ProductRuleEdit = () => {
    const [description, setDescription] = useState("");

    const transform = (data: any) => {
        return non_duplicate_transform(data, description);
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />} validate={validateRuleForm}>
                <WithRecord
                    render={(product_rule) => (
                        <RuleEditComponent
                            product={product_rule.product_data}
                            initialStatus={product_rule ? product_rule.new_status : ""}
                            setDescription={setDescription}
                        />
                    )}
                />
            </SimpleForm>
        </Edit>
    );
};

export default ProductRuleEdit;
