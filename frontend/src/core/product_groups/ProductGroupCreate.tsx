import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import { Create, SimpleForm, required } from "react-admin";

import { TextInputWide } from "../../commons/layout/themes";

const ProductGroupCreate = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <Typography variant="h6">ProductGroup</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />
            </SimpleForm>
        </Create>
    );
};

const requiredValidate = [required()];

export default ProductGroupCreate;
