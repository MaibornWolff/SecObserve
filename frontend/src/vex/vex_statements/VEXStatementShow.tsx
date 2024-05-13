import { Stack, Typography } from "@mui/material";
import {
    ChipField,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

const ShowActions = () => {
    const vex_statement = useRecordContext();

    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {vex_statement && (
                    <PrevNextButtons
                        linkType="show"
                        filter={{ document: vex_statement.document }}
                        sort={{ field: "vulnerability_id", order: "ASC" }}
                        storeKey="vex_statements.embedded"
                    />
                )}
            </Stack>
        </TopToolbar>
    );
};

const VEXStatementShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(vex_statement) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Imported VEX Statement</Typography>
                        <ReferenceField source="document" reference="vex/vex_documents" link="show">
                            <TextField source="document_id" />
                        </ReferenceField>
                        <TextField source="vulnerability_id" label="Vulnerability ID" />
                        <ChipField source="status" />
                        {vex_statement.justification && <TextField source="justification" />}
                        {vex_statement.impact && <TextField source="impact" />}
                        {vex_statement.remediation && <TextField source="remediation" />}
                        {vex_statement.product_id && <TextField source="product_id" label="Product ID" />}
                        {vex_statement.product_purl && <TextField source="product_purl" label="Product PURL" />}
                        {vex_statement.product_cpe23 && <TextField source="product_cpe23" label="Product CPE" />}
                        {vex_statement.component_id && <TextField source="component_id" label="Component ID" />}
                        {vex_statement.component_purl && <TextField source="component_purl" label="Component PURL" />}
                        {vex_statement.component_cpe23 && <TextField source="component_cpe23" label="Component CPE" />}
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default VEXStatementShow;
