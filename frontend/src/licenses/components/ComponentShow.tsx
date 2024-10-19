import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { Labeled, PrevNextButtons, Show, TextField, TopToolbar, WithRecord, useRecordContext } from "react-admin";

import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_component_purl_url } from "../../commons/functions";
import MermaidDependencies from "../../core/observations/Mermaid_Dependencies";
import { useStyles } from "../../commons/layout/themes";

const ShowActions = () => {
    const component = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {component && (
                    <PrevNextButtons
                        filter={{ component_license: Number(component.component_license) }}
                        linkType="show"
                        sort={{ field: "name_version", order: "ASC" }}
                        storeKey="components.embedded"
                    />
                )}
            </Stack>
        </TopToolbar>
    );
};

export const ComponentComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(component) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 1, padding: 2, height: "100%" }}>
                        <Stack spacing={1}>
                            <Typography variant="h6">Component</Typography>
                            <Stack direction="row" spacing={4}>
                                {component.name != "" && (
                                    <Labeled>
                                        <TextField source="name" label="Component name" className={classes.fontBigBold} />
                                    </Labeled>
                                )}
                                {component.version != "" && (
                                    <Labeled>
                                        <TextField source="version" label="Component version" className={classes.fontBigBold} />
                                    </Labeled>
                                )}
                            </Stack>
                            {component.purl != "" &&
                                    get_component_purl_url(
                                        component.name,
                                        component.version,
                                        component.purl_type,
                                        component.purl_namespace
                                    ) == null && (
                                        <Labeled>
                                            <TextField source="purl" label="Component PURL" />
                                        </Labeled>
                                    )}
                                {component.purl != "" &&
                                    get_component_purl_url(
                                        component.name,
                                        component.version,
                                        component.purl_type,
                                        component.purl_namespace
                                    ) != null && (
                                        <Labeled>
                                            <TextUrlField
                                                label="Component PURL"
                                                text={component.purl}
                                                url={
                                                    component.purl &&
                                                    get_component_purl_url(
                                                        component.name,
                                                        component.version,
                                                        component.purl_type,
                                                        component.purl_namespace
                                                    )
                                                }
                                            />
                                        </Labeled>
                                    )}
                                {component.cpe != "" && (
                                    <Labeled>
                                        <TextField source="cpe" label="Component CPE" />
                                    </Labeled>
                                )}
                            {component.dependencies != "" && (
                                <MermaidDependencies
                                    dependencies={component.dependencies}
                                    needs_initialization={true}
                                />
                            )}
                        </Stack>
                    </Paper>
                </Box>
            )}
        />
    );
};

const ComponentShow = () => {
    return (
        <Show actions={<ShowActions />} component={ComponentComponent}>
            <Fragment />
        </Show>
    );
};

export default ComponentShow;
