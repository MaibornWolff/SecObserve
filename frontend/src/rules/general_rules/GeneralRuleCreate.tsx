import { Create, SimpleForm } from "react-admin";

import { OBSERVATION_STATUS_OPEN } from "../../core/types";
import { RuleCreateEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const GeneralRuleCreate = () => {
    const transform = (data: any) => {
        return non_duplicate_transform(data);
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges validate={validateRuleForm}>
                <RuleCreateEditComponent product={null} initialStatus={OBSERVATION_STATUS_OPEN} />{" "}
            </SimpleForm>
        </Create>
    );
};

export default GeneralRuleCreate;
