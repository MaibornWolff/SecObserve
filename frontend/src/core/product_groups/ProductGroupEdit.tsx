import { Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, required, useRecordContext } from "react-admin";

import { PERMISSION_PRODUCT_DELETE } from "../../access_control/types";
import { TextInputWide } from "../../commons/layout/themes";

const CustomToolbar = () => {
    const product = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            {product && product.permissions.includes(PERMISSION_PRODUCT_DELETE) && (
                <DeleteButton mutationMode="pessimistic" />
            )}
        </Toolbar>
    );
};

const ProductGroupEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6">ProductGroup</Typography>
                <TextInputWide autoFocus source="name" validate={requiredValidate} />
                <RichTextInput source="description" />
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ProductGroupEdit;
