import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    ChipField,
    DateField,
    Labeled,
    PrevNextButtons,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import VEXStatementEmbeddedList from "../vex_statements/VEXStatementEmbeddedList";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "document_id", order: "ASC" }}
                    storeKey="vex_documents.list"
                />
            </Stack>
        </TopToolbar>
    );
};

const VEXDocumentComponent = () => {
    return (
        <WithRecord
            render={(vex_document) => (
                <SimpleShowLayout>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6">Imported VEX Document</Typography>
                        <Stack spacing={1}>
                            <Labeled label="Type">
                                <ChipField
                                    source="type"
                                    sx={{
                                        width: "fit-content",
                                    }}
                                />
                            </Labeled>
                            <Labeled label="Document ID">
                                <TextField source="document_id" label="Document ID" />
                            </Labeled>
                            <Labeled label="Version">
                                <TextField source="version" />
                            </Labeled>
                            <Labeled label="Current release date">
                                <DateField source="current_release_date" showTime />
                            </Labeled>
                            <Labeled label="Initial release date">
                                <DateField source="initial_release_date" showTime />
                            </Labeled>
                            <Labeled label="Author">
                                <TextField source="author" />
                            </Labeled>
                            {vex_document && vex_document.role && (
                                <Labeled label="Role">
                                    <TextField source="role" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Statements
                        </Typography>
                        <VEXStatementEmbeddedList vex_document={vex_document} />
                    </Paper>
                </SimpleShowLayout>
            )}
        />
    );
};

const VEXDocumentShow = () => {
    return (
        <Show actions={<ShowActions />} component={VEXDocumentComponent}>
            <Fragment />
        </Show>
    );
};

export default VEXDocumentShow;
