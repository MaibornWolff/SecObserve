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

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "tracking_initial_release_date", order: "DESC" }}
                    storeKey="csaf.list"
                />
                <DeleteWithConfirmButton />
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
                        <Typography variant="h6">CSAF</Typography>
                        {csaf && csaf.product_name && (
                            <ReferenceField source="product" reference="products" link="show" />
                        )}
                        {csaf && csaf.vulnerability_names && (
                            <TextField source="vulnerability_names" label="Vulnerabilities" />
                        )}
                        <TextField source="user_full_name" />
                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                        <Typography variant="h6">Document</Typography>{" "}
                        <TextField source="document_id_prefix" label="ID prefix" />
                        <TextField source="document_base_id" label="Base ID" />
                        <TextField source="version" />
                        <TextField source="document_id" label="Document ID" />
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
