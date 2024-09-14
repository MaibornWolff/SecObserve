import { Fragment } from "react";
import {
    BulkDeleteButton,
    CreateButton,
    Datagrid,
    FunctionField,
    List,
    NullableBooleanInput,
    ReferenceInput,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import products from ".";
import { PERMISSION_PRODUCT_CREATE } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { humanReadableDate } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { Product } from "../types";
import { AGE_CHOICES } from "../types";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <ReferenceInput source="product_group" reference="product_groups" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <NullableBooleanInput source="security_gate_passed" alwaysOn />,
    <AutocompleteInputMedium source="age" choices={AGE_CHOICES} label="Last observation change" alwaysOn />,
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
            {user && JSON.parse(user).permissions.includes(PERMISSION_PRODUCT_CREATE) && <CreateButton />}
        </TopToolbar>
    );
};

const ProductList = () => {
    localStorage.removeItem("productembeddedlist.product_group");

    return (
        <Fragment>
            <ListHeader icon={products.icon} title="Products" />
            <List
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "name", order: "ASC" }}
                actions={<ListActions />}
                disableSyncWithLocation={false}
                storeKey="products.list"
            >
                <Datagrid size={getSettingListSize()} rowClick="show" bulkActionButtons={<BulkActionButtons />}>
                    <TextField source="name" />
                    <TextField source="product_group_name" label="Product Group" />
                    <TextField
                        source="repository_default_branch_name"
                        label="Default branch / version"
                        sortable={false}
                    />
                    <SecurityGateTextField label="Security gate" />
                    <ObservationsCountField label="Open observations" withLabel={false} />
                    <FunctionField<Product>
                        label="Last observation change"
                        sortBy="last_observation_change"
                        render={(record) => (record ? humanReadableDate(record.last_observation_change) : "")}
                    />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default ProductList;
