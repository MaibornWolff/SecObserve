import { Fragment } from "react";
import { Datagrid, FunctionField, List, NumberField, ReferenceInput, TextField, TextInput } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { humanReadableDate } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/settings/functions";
import openvex from "../../vex/openvex";
import { OpenVEX } from "../../vex/types";

const listFilters = [
    <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <TextInput source="vulnerability_names__name" label="Vulnerability" alwaysOn />,
];

const OpenVEXList = () => {
    return (
        <Fragment>
            <ListHeader icon={openvex.icon} title="VEX / OpenVEX" />
            <List
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "timestamp", order: "DESC" }}
                actions={false}
                disableSyncWithLocation={false}
                storeKey="openvex.list"
            >
                <Datagrid size={getSettingListSize()} rowClick="show" bulkActionButtons={false}>
                    <TextField source="product_name" label="Product" />
                    <TextField source="vulnerability_names" label="Vulnerabilities" sortable={false} />
                    <TextField source="document_id_prefix" label="ID prefix" />
                    <TextField source="document_base_id" label="Base ID" />
                    <NumberField source="version" label="Version" />
                    <TextField source="author" label="Author" />
                    <FunctionField<OpenVEX>
                        label="Created"
                        sortBy="timestamp"
                        render={(record) => (record ? humanReadableDate(record.timestamp) : "")}
                    />
                    <FunctionField<OpenVEX>
                        label="Updated"
                        sortBy="last_updated"
                        render={(record) => (record ? humanReadableDate(record.last_updated) : "")}
                    />
                    <TextField source="user_full_name" label="User" />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default OpenVEXList;
