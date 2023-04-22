import { Box, Paper, Typography } from "@mui/material";
import {
    ArrayField,
    Datagrid,
    DateField,
    Labeled,
    ReferenceField,
    SimpleShowLayout,
    TextField,
    UrlField,
    WithRecord,
} from "react-admin";
import { Link } from "react-router-dom";

import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { useStyles } from "../../commons/layout/themes";

const ObservationsShowAside = () => {
    return (
        <Box width={"33%"} ml={2}>
            <MetaData />
            <References />
            <Evidences />
        </Box>
    );
};

const MetaData = () => {
    return (
        <Paper sx={{ mb: 2 }}>
            <WithRecord
                render={(observation) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Metadata</Typography>
                        <ReferenceField source="product" reference="products" link="show" />
                        <ReferenceField source="parser" reference="parsers" label="Parser name" link="show" />
                        <ReferenceField source="parser" reference="parsers" label="Parser type" link={false}>
                            <TextField source="type" />
                        </ReferenceField>
                        <ReferenceField source="parser" reference="parsers" label="Parser source" link={false}>
                            <TextField source="source" />
                        </ReferenceField>
                        {observation.scanner_observation_id != "" && (
                            <TextField source="scanner_observation_id" label="Scanner observation id" />
                        )}
                        {observation.scanner != "" && <TextField source="scanner" />}
                        {observation.upload_filename != "" && <TextField source="upload_filename" />}
                        {observation.api_configuration_name != "" && (
                            <TextField source="api_configuration_name" label="API configuration" />
                        )}
                        {observation.general_rule != null && (
                            <ReferenceField
                                source="general_rule"
                                reference="general_rules"
                                label="General rule name"
                                link="show"
                            />
                        )}
                        {observation.product_rule != null && (
                            <ReferenceField
                                source="product_rule"
                                reference="product_rules"
                                label="Product rule name"
                                link="show"
                            />
                        )}
                        {observation.issue_tracker_issue_id != "" && (
                            <Labeled label="Issue">
                                <TextUrlField
                                    text={
                                        observation.product_data.issue_tracker_type +
                                        " #" +
                                        observation.issue_tracker_issue_id
                                    }
                                    url={observation.issue_tracker_issue_url}
                                />
                            </Labeled>
                        )}
                        <DateField source="import_last_seen" showTime />
                        <DateField source="created" showTime />
                    </SimpleShowLayout>
                )}
            />
        </Paper>
    );
};

const References = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(observation) => (
                <div>
                    {" "}
                    {observation.references && observation.references.length > 0 && (
                        <Paper>
                            <Typography
                                variant="h6"
                                sx={{
                                    paddingLeft: "16px",
                                    paddingTop: "8px",
                                }}
                            >
                                References
                            </Typography>
                            <ArrayField source="references" label={false}>
                                <Datagrid bulkActionButtons={false}>
                                    <UrlField source="url" label={false} target="_blank" className={classes.link} />
                                </Datagrid>
                            </ArrayField>
                        </Paper>
                    )}{" "}
                </div>
            )}
        />
    );
};

const Evidences = () => {
    const { classes } = useStyles();
    return (
        <WithRecord
            render={(observation) => (
                <div>
                    {" "}
                    {observation.evidences && observation.evidences.length > 0 && (
                        <Paper
                            sx={{
                                marginTop: "16px",
                            }}
                        >
                            <Typography
                                variant="h6"
                                sx={{
                                    paddingLeft: "16px",
                                    paddingTop: "8px",
                                }}
                            >
                                Evidences
                            </Typography>
                            <ArrayField source="evidences" label={false}>
                                <Datagrid bulkActionButtons={false}>
                                    <WithRecord
                                        render={(evidence) => (
                                            <Link to={"/evidences/" + evidence.id + "/show"} className={classes.link}>
                                                {evidence.name}
                                            </Link>
                                        )}
                                    />
                                </Datagrid>
                            </ArrayField>
                        </Paper>
                    )}{" "}
                </div>
            )}
        />
    );
};

export default ObservationsShowAside;
