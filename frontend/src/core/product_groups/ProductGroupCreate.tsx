import { Create, SimpleForm } from "react-admin";

import { transform_product_group_and_product } from "../functions";
import { ProductGroupCreateEditComponent } from "./functions";

const ProductGroupCreate = () => {
    return (
        <Create redirect="show" transform={transform_product_group_and_product}>
            <SimpleForm warnWhenUnsavedChanges>
                <ProductGroupCreateEditComponent />{" "}
            </SimpleForm>
        </Create>
    );
};

export default ProductGroupCreate;
