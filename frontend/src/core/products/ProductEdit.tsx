import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, useRecordContext } from "react-admin";

import { PERMISSION_PRODUCT_DELETE } from "../../access_control/types";
import { ProductCreateEditComponent, transform } from "./functions";

const CustomToolbar = () => {
    const product = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            {product?.permissions.includes(PERMISSION_PRODUCT_DELETE) && <DeleteButton mutationMode="pessimistic" />}
        </Toolbar>
    );
};

const ProductEdit = () => {
    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <ProductCreateEditComponent edit={true} />
            </SimpleForm>
        </Edit>
    );
};

export default ProductEdit;
