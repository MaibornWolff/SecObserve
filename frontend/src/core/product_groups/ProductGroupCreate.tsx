import { useState } from "react";
import { Create, SimpleForm } from "react-admin";

import { transform_product_group_and_product } from "../functions";
import { ProductGroupCreateEditComponent } from "./functions";

const ProductGroupCreate = () => {
    const [description, setDescription] = useState("");

    const transform = (data: any) => {
        return transform_product_group_and_product(data, description);
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <ProductGroupCreateEditComponent initialDescription="" setDescription={setDescription} />{" "}
            </SimpleForm>
        </Create>
    );
};

export default ProductGroupCreate;
