import { Create, SimpleForm } from "react-admin";

import { ProductCreateEditComponent, transform } from "./functions";

const ProductCreate = () => {
    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <ProductCreateEditComponent edit={false} />
            </SimpleForm>
        </Create>
    );
};

export default ProductCreate;
