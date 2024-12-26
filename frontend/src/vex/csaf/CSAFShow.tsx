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
import CSAFUpdate from "./CSAFUpdate";

const ShowActions = () => {
    const csaf = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "tracking_initial_release_date", order: "DESC" }}
                    storeKey="csaf.list"
                />
                {update_permission(csaf) && <CSAFUpdate />}
                {delete_permission(csaf) && <DeleteWithConfirmButton />}
            </Stack>
        </TopToolbar>
    );
};

const CSAFShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(csaf) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Exported CSAF document</Typography>
                        {csaf && csaf.product_data && csaf.product_data.name && (
                            <ReferenceField
                                source="product"
                                reference="products"
                                queryOptions={{ meta: { api_resource: "product_names" } }}
                                link="show"
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        )}
                        {csaf && csaf.vulnerability_names && (
                            <ReferenceManyField
                                reference="vex/csaf_vulnerabilities"
                                target="csaf"
                                label="Vulnerabilities"
                            >
                                <SingleFieldList linkType={false}>
                                    <ChipField source="name" />
                                </SingleFieldList>
                            </ReferenceManyField>
                        )}
                        {csaf && csaf.branch_names && (
                            <ReferenceManyField reference="vex/csaf_branches" target="csaf" label="Branches / Versions">
                                <SingleFieldList linkType={false}>
                                    <ChipField source="name" />
                                </SingleFieldList>
                            </ReferenceManyField>
                        )}
                        <TextField source="user_full_name" label="User" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Document</Typography>{" "}
                        <TextField source="document_id_prefix" label="ID prefix" />
                        <TextField source="document_base_id" label="Base ID" />
                        <TextField source="version" />
                        <TextField source="title" />
                        <TextField source="tlp_label" label="TLP label" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Tracking</Typography>
                        <DateField
                            source="tracking_initial_release_date"
                            showTime={true}
                            label="Initial release date"
                        />
                        <DateField
                            source="tracking_current_release_date"
                            showTime={true}
                            label="Current release date"
                        />
                        <TextField source="tracking_status" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Publisher</Typography>
                        <TextField source="publisher_name" />
                        <TextField source="publisher_category" />
                        <TextField source="publisher_namespace" />
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default CSAFShow;
