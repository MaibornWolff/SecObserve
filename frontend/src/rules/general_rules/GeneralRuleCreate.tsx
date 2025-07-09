import { useState } from "react";
import { Create, SimpleForm } from "react-admin";

import { OBSERVATION_STATUS_OPEN } from "../../core/types";
import { RuleCreateEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

const GeneralRuleCreate = () => {
    const [description, setDescription] = useState("");

    const transform = (data: any) => {
        return non_duplicate_transform(data, description);
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges validate={validateRuleForm}>
                <RuleCreateEditComponent
                    product={null}
                    initialStatus={OBSERVATION_STATUS_OPEN}
                    initialDescription=""
                    setDescription={setDescription}
                />{" "}
            </SimpleForm>
        </Create>
    );
};

export default GeneralRuleCreate;
