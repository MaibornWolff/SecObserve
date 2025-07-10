import { useState } from "react";
import { Create, SimpleForm } from "react-admin";

import { ProductCreateEditComponent, transform } from "./functions";

const ProductCreate = () => {
    const [description, setDescription] = useState("");

    const create_transform = (data: any) => {
        return transform(data, description);
    };

    return (
        <Create redirect="show" transform={create_transform}>
            <SimpleForm warnWhenUnsavedChanges>
                <ProductCreateEditComponent edit={false} initialDescription="" setDescription={setDescription} />
            </SimpleForm>
        </Create>
    );
};

export default ProductCreate;
