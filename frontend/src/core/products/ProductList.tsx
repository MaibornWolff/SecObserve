import {
    List,
    Datagrid,
    TextField,
    TextInput,
    BulkDeleteButton,
    NullableBooleanInput,
    CreateButton,
    TopToolbar,
} from "react-admin";
import { Fragment } from "react";

import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { PERMISSION_PRODUCT_CREATE } from "../../access_control/types";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <NullableBooleanInput source="security_gate_passed" alwaysOn />,
];

const BulkActionButtons = () => (
    <Fragment>
        <BulkDeleteButton mutationMode="pessimistic" />
    </Fragment>
);

const ListActions = () => {
    const user = localStorage.getItem("user");
    return (
        <TopToolbar>
            {user &&
                JSON.parse(user).permissions.includes(
                    PERMISSION_PRODUCT_CREATE
                ) && <CreateButton />}
        </TopToolbar>
    );
};

const ProductList = () => {
    return (
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={<ListActions />}
            disableSyncWithLocation={false}
        >
            <Datagrid
                size="medium"
                rowClick="show"
                bulkActionButtons={<BulkActionButtons />}
            >
                <TextField source="name" />
                <SecurityGateTextField />
                <ObservationsCountField withLabel={false} />
            </Datagrid>
        </List>
    );
};

export default ProductList;
