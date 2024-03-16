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

import { PERMISSION_VEX_DELETE, PERMISSION_VEX_EDIT } from "../../access_control/types";
import OpenVEXUpdate from "./OpenVEXUpdate";

const ShowActions = () => {
    const open_vex = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons linkType="show" sort={{ field: "timestamp", order: "DESC" }} storeKey="openvex.list" />
                {open_vex &&
                    open_vex.product_data.permissions &&
                    open_vex.product_data.permissions.includes(PERMISSION_VEX_EDIT) && <OpenVEXUpdate />}
                {open_vex &&
                    open_vex.product_data.permissions &&
                    open_vex.product_data.permissions.includes(PERMISSION_VEX_DELETE) && <DeleteWithConfirmButton />}
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
                        {openvex && openvex.product_data.name && (
                            <ReferenceField source="product" reference="products" link="show" />
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
