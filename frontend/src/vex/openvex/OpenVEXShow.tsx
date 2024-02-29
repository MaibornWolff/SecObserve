import { Divider, Stack, Typography } from "@mui/material";
import {
    DateField,
    DeleteWithConfirmButton,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import OpenVEXUpdate from "./OpenVEXUpdate";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons linkType="show" sort={{ field: "timestamp", order: "DESC" }} storeKey="openvex.list" />
                <OpenVEXUpdate />
                <DeleteWithConfirmButton />
            </Stack>
        </TopToolbar>
    );
};

const OpenVEXShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(openvex) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">OpenVEX</Typography>
                        {openvex && openvex.product_name && (
                            <ReferenceField source="product" reference="products" link="show" />
                        )}
                        {openvex && openvex.vulnerability_names && (
                            <TextField source="vulnerability_names" label="Vulnerabilities" />
                        )}
                        <TextField source="user_full_name" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Document</Typography>{" "}
                        <TextField source="document_id_prefix" label="ID prefix" />
                        <TextField source="document_base_id" label="Base ID" />
                        <TextField source="version" />
                        <TextField source="document_id" label="Document ID" />
                        <TextField source="author" />
                        <TextField source="role" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Tracking</Typography>
                        <DateField source="timestamp" showTime={true} />
                        <DateField source="last_updated" showTime={true} />
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default OpenVEXShow;
