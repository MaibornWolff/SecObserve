import { Fragment } from "react";
import { Datagrid, DateField, List, TextField, TextInput } from "react-admin";

import vex_documents from ".";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ListHeader from "../../commons/layout/ListHeader";
import { getSettingListSize } from "../../commons/user_settings/functions";

const listFilters = [
    <TextInput source="document_id" label="Document ID" alwaysOn />,
    <TextInput source="author" alwaysOn />,
];

const VEXDocumentList = () => {
    return (
        <Fragment>
            <ListHeader icon={vex_documents.icon} title="Imported VEX Documents" />
            <List
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "document_id", order: "ASC" }}
                actions={false}
                disableSyncWithLocation={false}
                storeKey="vex_documents.list"
            >
                <Datagrid size={getSettingListSize()} rowClick="show">
                    <TextField source="type" />
                    <TextField source="document_id" label="Document ID" />
                    <TextField source="version" />
                    <DateField source="current_release_date" label="Current release" />
                    <TextField source="author" />
                    <TextField source="role" />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default VEXDocumentList;
