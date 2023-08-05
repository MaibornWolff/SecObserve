import { CreateButton, Datagrid, List, TextField, TextInput, TopToolbar } from "react-admin";

import { PERMISSION_PRODUCT_GROUP_CREATE } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";

const listFilters = [<TextInput source="name" alwaysOn />];

const ListActions = () => {
    const user = localStorage.getItem("user");
    return (
        <TopToolbar>
            {user && JSON.parse(user).permissions.includes(PERMISSION_PRODUCT_GROUP_CREATE) && <CreateButton />}
        </TopToolbar>
    );
};

const ProductGroupList = () => {
    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={<ListActions />}
            disableSyncWithLocation={false}
        >
            <Datagrid size="medium" rowClick="show" bulkActionButtons={false}>
                <TextField source="name" />
                <TextField source="products_count" label="Products" />
                <ObservationsCountField withLabel={false} />
            </Datagrid>
        </List>
    );
};

export default ProductGroupList;
