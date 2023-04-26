import { JsonViewer, JsonViewerTheme } from "@textea/json-viewer";
import { Labeled, ReferenceField, Show, SimpleShowLayout, TextField, WithRecord } from "react-admin";

import { useStyles } from "../../commons/layout/themes";
import { getSettingTheme } from "../../commons/settings/functions";

const EvidenceShow = () => {
    const { classes } = useStyles();
    return (
        <Show>
            <SimpleShowLayout>
                <ReferenceField source="product" reference="products" link="show">
                    <TextField source="name" />
                </ReferenceField>
                <ReferenceField source="observation" reference="observations" link="show">
                    <TextField source="title" />
                </ReferenceField>
                <TextField source="name" />
                <WithRecord
                    render={(evidence) => (
                        <Labeled label="Evidence">
                            <JsonViewer
                                value={JSON.parse(evidence.evidence)}
                                groupArraysAfterLength={10000}
                                displayDataTypes={false}
                                displaySize={false}
                                indentWidth={4}
                                collapseStringsAfterLength={false}
                                enableClipboard={false}
                                className={classes.displayFontSize}
                                theme={getSettingTheme() as JsonViewerTheme}
                            />
                        </Labeled>
                    )}
                />
            </SimpleShowLayout>
        </Show>
    );
};

export default EvidenceShow;
