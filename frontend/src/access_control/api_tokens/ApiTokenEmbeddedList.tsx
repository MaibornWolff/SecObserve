import {
    Datagrid,
    ListContextProvider,
    ResourceContextProvider,
    SelectField,
    SortPayload,
    TextField,
    WithRecord,
    useListController,
} from "react-admin";
import { Fragment } from "react/jsx-runtime";

import { PERMISSION_PRODUCT_API_TOKEN_REVOKE, ROLE_CHOICES } from "../../access_control/types";
import { getSettingListSize } from "../../commons/user_settings/functions";
import ApiTokenRevoke from "./ApiTokenRevoke";

type ApiTokenEmbeddedListProps = {
    type: "user" | "product";
    product?: any;
    user?: any;
};

const ApiTokenEmbeddedList = ({ type, product, user }: ApiTokenEmbeddedListProps) => {
    const filter = type === "product" ? { product: Number(product.id) } : { user: Number(user.id) };
    const sort: SortPayload = type === "product" ? { field: "role", order: "ASC" } : { field: "user", order: "ASC" };
    const resource = type === "product" ? "product_api_tokens" : "api_tokens";
    const current_user = localStorage.getItem("user");
    const username = current_user ? JSON.parse(current_user).username : "";

    const listContext = useListController({
        filter: filter,
        perPage: 25,
        resource: resource,
        sort: sort,
        disableSyncWithLocation: true,
        storeKey: "api_tokens.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value={resource}>
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                        rowClick={false}
                    >
                        {type === "product" && <SelectField source="role" choices={ROLE_CHOICES} />}
                        {type === "user" && <TextField label="Username" source="name" />}
                        <WithRecord
                            render={(api_token) => (
                                <Fragment>
                                    {((type === "product" &&
                                        product?.permissions.includes(PERMISSION_PRODUCT_API_TOKEN_REVOKE)) ||
                                        (type === "user" && api_token.name === username)) && (
                                        <ApiTokenRevoke type={type} product={product} user={user} />
                                    )}
                                </Fragment>
                            )}
                        />
                    </Datagrid>
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default ApiTokenEmbeddedList;
