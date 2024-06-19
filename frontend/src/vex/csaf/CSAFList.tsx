import { Fragment } from "react";
import {
    ChipField,
    Datagrid,
    FunctionField,
    List,
    NumberField,
    ReferenceInput,
    ReferenceManyField,
    SingleFieldList,
    TextField,
    TextInput,
    TopToolbar,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { humanReadableDate } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import csaf from "../../vex/csaf";
import { CSAF } from "../../vex/types";
import CSAFCreate from "./CSAFCreate";

const listFilters = [
    <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
    <TextInput source="vulnerability_names__name" label="Vulnerability" alwaysOn />,
];

const ListActions = () => (
    <TopToolbar>
        <CSAFCreate />
    </TopToolbar>
);

const CSAFList = () => {
    return (
        <Fragment>
            <ListHeader icon={csaf.icon} title="Exported CSAF documents" />
            <List
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "tracking_initial_release_date", order: "DESC" }}
                actions={<ListActions />}
                disableSyncWithLocation={false}
                storeKey="csaf.list"
                empty={false}
            >
                <Datagrid size={getSettingListSize()} rowClick="show" bulkActionButtons={false}>
                    <TextField source="product_data.name" label="Product" />
                    <ReferenceManyField reference="vex/csaf_vulnerabilities" target="csaf" label="Vulnerabilities">
                        <SingleFieldList linkType={false}>
                            <ChipField source="name" />
                        </SingleFieldList>
                    </ReferenceManyField>
                    <ReferenceManyField reference="vex/csaf_branches" target="csaf" label="Branches / Versions">
                        <SingleFieldList linkType={false}>
                            <ChipField source="name" />
                        </SingleFieldList>
                    </ReferenceManyField>
                    <TextField source="document_id_prefix" label="ID prefix" />
                    <TextField source="document_base_id" label="Base ID" />
                    <NumberField source="version" label="Version" />
                    <TextField source="title" />
                    <TextField source="publisher_name" label="Pub. name" />
                    <FunctionField<CSAF>
                        label="Created"
                        sortBy="tracking_initial_release_date"
                        render={(record) => (record ? humanReadableDate(record.tracking_initial_release_date) : "")}
                    />
                    <FunctionField<CSAF>
                        label="Updated"
                        sortBy="tracking_current_release_date"
                        render={(record) => (record ? humanReadableDate(record.tracking_current_release_date) : "")}
                    />
                    <TextField source="user_full_name" label="User" />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default CSAFList;
