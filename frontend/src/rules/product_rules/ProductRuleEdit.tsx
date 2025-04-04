import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, WithRecord, useRecordContext } from "react-admin";

import { PERMISSION_PRODUCT_RULE_DELETE } from "../../access_control/types";
import { RuleCreateEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const CustomToolbar = () => {
    const rule = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
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
    const transform = (data: any) => {
        return non_duplicate_transform(data);
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <ProductRuleEditForm />
        </Edit>
    );
};
const ProductRuleEditForm = () => {
    return (
        <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />} validate={validateRuleForm}>
            <WithRecord
                render={(product_rule) => (
                    <RuleCreateEditComponent
                        product={product_rule.product_data}
                        initialStatus={product_rule ? product_rule.new_status : ""}
                    />
                )}
            />
        </SimpleForm>
    );
};

export default ProductRuleEdit;
