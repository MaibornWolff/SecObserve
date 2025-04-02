import { Create, SimpleForm } from "react-admin";

import { ProductGroupCreateEditComponent, transform } from "./functions";

const ProductGroupCreate = () => {
    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <ProductGroupCreateEditComponent />{" "}
            </SimpleForm>
        </Create>
    );
};

export default ProductGroupCreate;
