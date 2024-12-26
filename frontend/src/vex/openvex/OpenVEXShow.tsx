import { Divider, Stack, Typography } from "@mui/material";
import {
    ChipField,
    DateField,
    DeleteWithConfirmButton,
    PrevNextButtons,
    ReferenceField,
    ReferenceManyField,
    Show,
    SimpleShowLayout,
    SingleFieldList,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { delete_permission, update_permission } from "../functions";
import OpenVEXUpdate from "./OpenVEXUpdate";

const ShowActions = () => {
    const openvex = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons linkType="show" sort={{ field: "timestamp", order: "DESC" }} storeKey="openvex.list" />
                {update_permission(openvex) && <OpenVEXUpdate />}
                {delete_permission(openvex) && <DeleteWithConfirmButton />}
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
                        <Typography variant="h6">Exported OpenVEX document</Typography>
                        {openvex && openvex.product_data && openvex.product_data.name && (
                            <ReferenceField
                                source="product"
                                reference="products"
                                queryOptions={{ meta: { api_resource: "product_names" } }}
                                link="show"
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        )}
                        {openvex && openvex.vulnerability_names && (
                            <ReferenceManyField
                                reference="vex/openvex_vulnerabilities"
                                target="openvex"
                                label="Vulnerabilities"
                            >
                                <SingleFieldList linkType={false}>
                                    <ChipField source="name" />
                                </SingleFieldList>
                            </ReferenceManyField>
                        )}
                        {openvex && openvex.branch_names && (
                            <ReferenceManyField
                                reference="vex/openvex_branches"
                                target="openvex"
                                label="Branches / Versions"
                            >
                                <SingleFieldList linkType={false}>
                                    <ChipField source="name" />
                                </SingleFieldList>
                            </ReferenceManyField>
                        )}
                        <TextField source="user_full_name" label="User" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Document</Typography>{" "}
                        <TextField source="id_namespace" label="ID namespace" />
                        <TextField source="document_id_prefix" label="ID prefix" />
                        <TextField source="document_base_id" label="Base ID" />
                        <TextField source="version" />
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
