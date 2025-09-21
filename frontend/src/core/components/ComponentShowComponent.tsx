import { Stack, Typography } from "@mui/material";
import { Labeled, RecordContextProvider, TextField, useRecordContext } from "react-admin";

import components from ".";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { feature_vex_enabled, get_component_purl_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import MermaidDependencies from "../observations/Mermaid_Dependencies";

type ComponentShowComponentProps = {
    component?: any;
};

const ComponentShowComponent = ({ component }: ComponentShowComponentProps) => {
    const { classes } = useStyles();

    const component_record = useRecordContext();
    if (!component) {
        component = component_record;
    }

    return (
        <RecordContextProvider value={component}>
            {component && (
                <Stack spacing={1}>
                    <Typography variant="h6">
                        <components.icon />
                        &nbsp;&nbsp;Component
                    </Typography>
                    <Stack direction="row" spacing={4}>
                        {component.component_name != "" && (
                            <Labeled>
                                <TextField source="component_name" label="Name" className={classes.fontBigBold} />
                            </Labeled>
                        )}
                        {component.component_version != "" && (
                            <Labeled>
                                <TextField source="component_version" label="Version" className={classes.fontBigBold} />
                            </Labeled>
                        )}
                    </Stack>
                    {component.component_purl != "" &&
                        get_component_purl_url(
                            component.component_name,
                            component.component_version,
                            component.component_purl_type,
                            component.component_purl_namespace
                        ) == null && (
                            <Labeled>
                                <TextField source="component_purl" label="Component PURL" />
                            </Labeled>
                        )}
                    {component.component_purl != "" &&
                        get_component_purl_url(
                            component.component_name,
                            component.component_version,
                            component.component_purl_type,
                            component.component_purl_namespace
                        ) != null && (
                            <Labeled>
                                <TextUrlField
                                    label="PURL"
                                    text={component.component_purl}
                                    url={
                                        component.component_purl &&
                                        get_component_purl_url(
                                            component.component_name,
                                            component.component_version,
                                            component.component_purl_type,
                                            component.component_purl_namespace
                                        )
                                    }
                                    new_tab={true}
                                />
                            </Labeled>
                        )}
                    {component.component_cpe != "" && (
                        <Labeled>
                            <TextField source="component_cpe" label="CPE" />
                        </Labeled>
                    )}
                    {feature_vex_enabled() && component.component_cyclonedx_bom_link != "" && (
                        <Labeled>
                            <TextField source="component_cyclonedx_bom_link" label="CycloneDX BOM Link" />
                        </Labeled>
                    )}
                    {component.component_dependencies && component.component_dependencies != "" && (
                        <MermaidDependencies dependencies={component.component_dependencies} />
                    )}
                </Stack>
            )}
        </RecordContextProvider>
    );
};

export default ComponentShowComponent;
