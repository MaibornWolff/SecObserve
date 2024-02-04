import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    EditButton,
    Labeled,
    PrevNextButtons,
    ReferenceField,
    RichTextField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import { useStyles } from "../../commons/layout/themes";

const ShowActions = () => {
    const user = localStorage.getItem("user");
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons linkType="show" sort={{ field: "name", order: "ASC" }} storeKey="general_rules.list" />
                {user && JSON.parse(user).is_superuser && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const GeneralRuleComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(rule) => (
                <SimpleShowLayout>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Rule
                        </Typography>
                        <Stack spacing={1}>
                            <Labeled label="Name">
                                <TextField source="name" className={classes.fontBigBold} />
                            </Labeled>
                            {rule.description && (
                                <Labeled label="Description">
                                    <RichTextField source="description" />
                                </Labeled>
                            )}

                            {rule.new_severity && (
                                <Labeled label="New severity">
                                    <TextField source="new_severity" />
                                </Labeled>
                            )}
                            {rule.new_status && (
                                <Labeled label="New status">
                                    <TextField source="new_status" />
                                </Labeled>
                            )}
                            <Labeled label="Enabled">
                                <BooleanField source="enabled" />
                            </Labeled>
                        </Stack>
                    </Paper>

                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Observation
                        </Typography>
                        <Stack spacing={1}>
                            <Labeled label="Parser">
                                <ReferenceField source="parser" reference="parsers" link="show" />
                            </Labeled>
                            {rule.scanner_prefix && (
                                <Labeled label="Scanner prefix">
                                    <TextField source="scanner_prefix" />
                                </Labeled>
                            )}
                            {rule.title && (
                                <Labeled label="Title">
                                    <TextField source="title" />
                                </Labeled>
                            )}
                            {rule.description_observation && (
                                <Labeled label="Description">
                                    <TextField source="description_observation" />
                                </Labeled>
                            )}
                        </Stack>
                    </Paper>

                    {rule &&
                        (rule.origin_component_name_version ||
                            rule.origin_docker_image_name_tag ||
                            rule.origin_endpoint_url ||
                            rule.origin_service_name ||
                            rule.origin_source_file ||
                            rule.origin_cloud_qualified_resource) && (
                            <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                    Origins
                                </Typography>
                                <Stack spacing={1}>
                                    {rule.origin_component_name_version && (
                                        <Labeled label="Component name:version">
                                            <TextField source="origin_component_name_version" />
                                        </Labeled>
                                    )}
                                    {rule.origin_docker_image_name_tag && (
                                        <Labeled label="Docker image name:tag">
                                            <TextField source="origin_docker_image_name_tag" />
                                        </Labeled>
                                    )}
                                    {rule.origin_endpoint_url && (
                                        <Labeled label="Endpoint URL">
                                            <TextField source="origin_endpoint_url" />
                                        </Labeled>
                                    )}
                                    {rule.origin_service_name && (
                                        <Labeled label="Service name">
                                            <TextField source="origin_service_name" />
                                        </Labeled>
                                    )}
                                    {rule.origin_source_file && (
                                        <Labeled label="Source file">
                                            <TextField source="origin_source_file" />
                                        </Labeled>
                                    )}
                                    {rule.origin_cloud_qualified_resource && (
                                        <Labeled label="Cloud qualified resource">
                                            <TextField source="origin_cloud_qualified_resource" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Paper>
                        )}
                </SimpleShowLayout>
            )}
        />
    );
};

const GeneralRuleShow = () => {
    return (
        <Show actions={<ShowActions />} component={GeneralRuleComponent}>
            <Fragment />
        </Show>
    );
};

export default GeneralRuleShow;
