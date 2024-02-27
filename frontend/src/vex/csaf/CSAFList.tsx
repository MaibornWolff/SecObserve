import { ReferenceInput, Datagrid, List, TextField } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/settings/functions";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { Fragment } from "react";
import { Paper, Typography } from "@mui/material";
import csaf from '../../vex/csaf';

const listFilters = [
    <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }} alwaysOn>
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
];

const CSAFList = () => {
    return (
        <Fragment>
            <Paper sx={{                  padding: 2,
                    marginTop: 2,
}}>
                <Typography variant="h6" component="h2" align="left" alignItems="center" display={"flex"}>
                    <csaf.icon />&nbsp;&nbsp;VEX / CSAF
                </Typography>
            </Paper>
        <List
            perPage={25}
            pagination={<CustomPagination />}
            filters={listFilters}
            sort={{ field: "name", order: "ASC" }}
            actions={false}
            disableSyncWithLocation={false}
        >
            <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false}>
                <TextField source="product_name" label="Product" />
                <TextField source="document_id" />
                <TextField source="title" />
            </Datagrid>
        </List>
        </Fragment>
    );
};

export default CSAFList;
