import { JsonViewer, JsonViewerTheme } from "@textea/json-viewer";
import {
    Labeled,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import { useStyles } from "../../commons/layout/themes";
import { getSettingTheme } from "../../commons/settings/functions";

const ShowActions = () => {
    const observation_id = localStorage.getItem("observationshow.id");
    if (observation_id) {
        return (
            <TopToolbar>
                <PrevNextButtons
                    filter={{ observation: observation_id }}
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                />
            </TopToolbar>
        );
    } else {
        return null;
    }
};

const EvidenceShow = () => {
    const { classes } = useStyles();
    return (
        <Show actions={<ShowActions />}>
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
                        <Labeled label="Evidence" width={"100%"}>
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
                                sx={{ padding: 1 }}
                            />
                        </Labeled>
                    )}
                />
            </SimpleShowLayout>
        </Show>
    );
};

export default EvidenceShow;
