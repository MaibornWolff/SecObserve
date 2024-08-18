import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { Labeled, TextField, useRecordContext } from "react-admin";

import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_component_purl_url } from "../../commons/functions";
import { getElevation } from "../../metrics/functions";

type ObservationShowOriginsProps = {
    elevated: boolean;
};

const ObservationShowOrigins = ({ elevated }: ObservationShowOriginsProps) => {
    const observation = useRecordContext();
    return (
        <Fragment>
            {observation &&
                (observation.origin_service_name != "" ||
                    observation.origin_component_name != "" ||
                    observation.origin_docker_image_name != "" ||
                    observation.origin_endpoint_url != "" ||
                    observation.origin_source_file != "" ||
                    observation.origin_cloud_provider != "") && (
                    <Paper elevation={getElevation(elevated)} sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Origins</Typography>
                        {observation.origin_service_name != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Service
                                </Typography>
                                <Labeled>
                                    <TextField source="origin_service_name" label="Name" />
                                </Labeled>
                            </Fragment>
                        )}
                        {observation.origin_component_name != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Component
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_component_name != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_name" label="Component name" />
                                        </Labeled>
                                    )}
                                    {observation.origin_component_version != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_version" label="Component version" />
                                        </Labeled>
                                    )}
                                    {observation.origin_component_purl != "" &&
                                        get_component_purl_url(
                                            observation.origin_component_name,
                                            observation.origin_component_version,
                                            observation.origin_component_purl_type,
                                            observation.origin_component_purl_namespace
                                        ) == null && (
                                            <Labeled>
                                                <TextField source="origin_component_purl" label="Component PURL" />
                                            </Labeled>
                                        )}
                                    {observation.origin_component_purl != "" &&
                                        get_component_purl_url(
                                            observation.origin_component_name,
                                            observation.origin_component_version,
                                            observation.origin_component_purl_type,
                                            observation.origin_component_purl_namespace
                                        ) != null && (
                                            <Labeled label="Component PURL">
                                                <TextUrlField
                                                    text={observation.origin_component_purl}
                                                    url={
                                                        observation.origin_component_purl &&
                                                        get_component_purl_url(
                                                            observation.origin_component_name,
                                                            observation.origin_component_version,
                                                            observation.origin_component_purl_type,
                                                            observation.origin_component_purl_namespace
                                                        )
                                                    }
                                                />
                                            </Labeled>
                                        )}
                                    {observation.origin_component_cpe != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_cpe" label="Component CPE" />
                                        </Labeled>
                                    )}
                                </Stack>
                                {observation.origin_component_dependencies != "" && (
                                    <Labeled sx={{ marginTop: 2 }}>
                                        <TextField
                                            source="origin_component_dependencies"
                                            label="Component dependencies"
                                            sx={{ whiteSpace: "pre-line" }}
                                        />
                                    </Labeled>
                                )}
                            </Fragment>
                        )}
                        {observation.origin_docker_image_name != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Docker
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_docker_image_name != "" && (
                                        <Labeled>
                                            <TextField source="origin_docker_image_name" label="Docker image name" />
                                        </Labeled>
                                    )}
                                    {observation.origin_docker_image_tag != "" && (
                                        <Labeled>
                                            <TextField source="origin_docker_image_tag" label="Docker image tag" />
                                        </Labeled>
                                    )}
                                </Stack>
                                {observation.origin_docker_image_digest != "" && (
                                    <Labeled>
                                        <TextField source="origin_docker_image_digest" label="Docker image digest" />
                                    </Labeled>
                                )}
                            </Fragment>
                        )}
                        {observation.origin_endpoint_url != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Endpoint
                                </Typography>
                                {observation.origin_endpoint_url != "" && (
                                    <Labeled label="Endpoint URL">
                                        <TextUrlField
                                            text={observation.origin_endpoint_url}
                                            url={observation.origin_endpoint_url}
                                        />
                                    </Labeled>
                                )}
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_endpoint_scheme != "" && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_scheme" label="Endpoint scheme" />
                                        </Labeled>
                                    )}
                                    {observation.origin_endpoint_hostname != "" && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_hostname" label="Endpoint host" />
                                        </Labeled>
                                    )}
                                    {observation.origin_endpoint_port != null && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_port" label="Endpoint port" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Fragment>
                        )}
                        {observation.origin_source_file != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Source
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_source_file != "" && (
                                        <Labeled>
                                            <TextUrlField
                                                text={observation.origin_source_file}
                                                url={observation.origin_source_file_url}
                                                label="Source file"
                                            />
                                        </Labeled>
                                    )}
                                    {observation.origin_source_line_start != null && (
                                        <Labeled>
                                            <TextField source="origin_source_line_start" label="Source line start" />
                                        </Labeled>
                                    )}
                                    {observation.origin_source_line_end != null && (
                                        <Labeled>
                                            <TextField source="origin_source_line_end" label="Source line end" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Fragment>
                        )}
                        {observation.origin_cloud_provider != "" && (
                            <Fragment>
                                <Typography variant="subtitle1" sx={{ paddingTop: 1 }}>
                                    Cloud
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_cloud_provider != "" && (
                                        <Labeled>
                                            <TextField source="origin_cloud_provider" label="Provider" />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_account_subscription_project != "" && (
                                        <Labeled>
                                            <TextField
                                                source="origin_cloud_account_subscription_project"
                                                label="Account / Subscription / Project"
                                            />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_resource != "" && (
                                        <Labeled>
                                            <TextField source="origin_cloud_resource" label="Resource" />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_resource_type != "" && (
                                        <Labeled>
                                            <TextField source="origin_cloud_resource_type" label="Resource type" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Fragment>
                        )}
                    </Paper>
                )}
        </Fragment>
    );
};

export default ObservationShowOrigins;
