import { Box, Paper, Typography } from "@mui/material";
import { TableHead } from "@mui/material";
import { Fragment } from "react";
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
        <Box width={"33%"} marginLeft={2} marginRight={1}>
            <MetaData />
            <References />
            <Evidences />
        </Box>
    );
};

const MetaData = () => {
    return (
        <Paper sx={{ marginBottom: 2 }}>
            <WithRecord
                render={(observation) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Metadata</Typography>
                        <ReferenceField source="product" reference="products" link="show" />
                        {observation.branch && (
                            <ReferenceField source="branch" reference="branches" label="Branch" link={false} />
                        )}
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

const EmptyDatagridHeader = () => <TableHead />;

const References = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(observation) => (
                <Fragment>
                    {observation.references && observation.references.length > 0 && (
                        <Paper sx={{ marginBottom: 2 }}>
                            <Typography variant="h6" sx={{ paddingLeft: 2, paddingTop: 1 }}>
                                References
                            </Typography>
                            <ArrayField source="references" label={false}>
                                <Datagrid
                                    bulkActionButtons={false}
                                    header={EmptyDatagridHeader}
                                    sx={{ paddingBottom: 2 }}
                                >
                                    <UrlField source="url" label={false} target="_blank" className={classes.link} />
                                </Datagrid>
                            </ArrayField>
                        </Paper>
                    )}
                </Fragment>
            )}
        />
    );
};

const Evidences = () => {
    const { classes } = useStyles();
    return (
        <WithRecord
            render={(observation) => (
                <Fragment>
                    {observation.evidences && observation.evidences.length > 0 && (
                        <Paper sx={{ marginBottom: 2 }}>
                            <Typography variant="h6" sx={{ paddingLeft: 2, paddingTop: 1 }}>
                                Evidences
                            </Typography>
                            <ArrayField source="evidences" label={false}>
                                <Datagrid
                                    bulkActionButtons={false}
                                    header={EmptyDatagridHeader}
                                    sx={{ paddingBottom: 2 }}
                                >
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
                    )}
                </Fragment>
            )}
        />
    );
};

export default ObservationsShowAside;
