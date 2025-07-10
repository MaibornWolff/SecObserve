import { useState } from "react";
import { DeleteButton, Edit, SaveButton, SimpleForm, Toolbar, WithRecord, useRecordContext } from "react-admin";

import { PERMISSION_PRODUCT_DELETE } from "../../access_control/types";
import { transform_product_group_and_product } from "../functions";
import { ProductGroupCreateEditComponent } from "./functions";

const CustomToolbar = () => {
    const product = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton alwaysEnable />
            {product?.permissions.includes(PERMISSION_PRODUCT_DELETE) && <DeleteButton mutationMode="pessimistic" />}
        </Toolbar>
    );
};

const ProductGroupEdit = () => {
    const [description, setDescription] = useState("");

    const transform = (data: any) => {
        return transform_product_group_and_product(data, description);
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <WithRecord
                    render={(product_group) => (
                        <ProductGroupCreateEditComponent
                            initialDescription={product_group.description}
                            setDescription={setDescription}
                        />
                    )}
                />
            </SimpleForm>
        </Edit>
    );
};

export default ProductGroupEdit;
