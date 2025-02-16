import { Divider, Stack, Typography } from "@mui/material";
import { useState } from "react";
import { BooleanInput, Create, ReferenceInput, SimpleForm } from "react-admin";

import general_rules from ".";
import {
    validate_255,
    validate_513,
    validate_2048,
    validate_required_255,
    validate_required_2048,
} from "../../commons/custom_validators";
import { justificationIsEnabledForStatus } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../../core/types";
import { validateRuleForm } from "../functions";

const GeneralRuleCreate = () => {
    const [status, setStatus] = useState(OBSERVATION_STATUS_OPEN);
    const justificationEnabled = justificationIsEnabledForStatus(status);

    const transform = (data: any) => {
        if (data.scanner_prefix == null) {
            data.scanner_prefix = "";
        }
        if (data.title == null) {
            data.title = "";
        }
        if (data.description_observation == null) {
            data.description_observation = "";
        }
        if (data.origin_component_name_version == null) {
            data.origin_component_name_version = "";
        }
        if (data.origin_docker_image_name_tag == null) {
            data.origin_docker_image_name_tag = "";
        }
        if (data.origin_endpoint_url == null) {
            data.origin_endpoint_url = "";
        }
        if (data.origin_service_name == null) {
            data.origin_service_name = "";
        }
        if (data.origin_source_file == null) {
            data.origin_source_file = "";
        }
        if (data.origin_cloud_qualified_resource == null) {
            data.origin_cloud_qualified_resource = "";
        }
        if (data.origin_kubernetes_qualified_resource == null) {
            data.origin_kubernetes_qualified_resource = "";
        }
        if (data.new_severity == null) {
            data.new_severity = "";
        }
        if (data.new_status == null) {
            data.new_status = "";
        }
        if (!justificationEnabled || data.new_vex_justification == null) {
            data.new_vex_justification = "";
        }
        return data;
    };

    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges validate={validateRuleForm}>
                <Typography variant="h6" alignItems="center" display={"flex"} sx={{ marginBottom: 1 }}>
                    <general_rules.icon />
                    &nbsp;&nbsp;General Rule
                </Typography>
                <Stack>
                    <TextInputWide autoFocus source="name" validate={validate_required_255} />
                    <TextInputWide
                        source="description"
                        multiline
                        minRows={3}
                        helperText="Markdown supported. Description will be copied into the Observation Log."
                        validate={validate_required_2048}
                    />
                    <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                    <AutocompleteInputMedium
                        source="new_status"
                        choices={OBSERVATION_STATUS_CHOICES}
                        onChange={(e) => setStatus(e)}
                    />
                    {justificationEnabled && (
                        <AutocompleteInputMedium
                            label="New VEX justification"
                            source="new_vex_justification"
                            choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                        />
                    )}
                    <BooleanInput source="enabled" defaultValue={true} />
                </Stack>
                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Observation
                </Typography>
                <Stack>
                    <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }}>
                        <AutocompleteInputWide optionText="name" />
                    </ReferenceInput>
                    <TextInputWide source="scanner_prefix" validate={validate_255} />
                    <TextInputWide
                        source="title"
                        label="Title"
                        helperText="Regular expression to match the observation's title"
                        validate={validate_255}
                    />
                    <TextInputWide
                        source="description_observation"
                        label="Description"
                        helperText="Regular expression to match the observation's description"
                        validate={validate_255}
                    />
                </Stack>
                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Origins
                </Typography>
                <Stack>
                    <TextInputWide
                        source="origin_component_name_version"
                        label="Component name:version"
                        helperText="Regular expression to match the component name:version"
                        validate={validate_513}
                    />
                    <TextInputWide
                        source="origin_docker_image_name_tag"
                        label="Docker image name:tag"
                        helperText="Regular expression to match the docker image name:tag"
                        validate={validate_513}
                    />
                    <TextInputWide
                        source="origin_endpoint_url"
                        label="Endpoint URL"
                        helperText="Regular expression to match the endpoint URL"
                        validate={validate_2048}
                    />
                    <TextInputWide
                        source="origin_service_name"
                        label="Service name"
                        helperText="Regular expression to match the service name"
                        validate={validate_255}
                    />
                    <TextInputWide
                        source="origin_source_file"
                        label="Source file"
                        helperText="Regular expression to match the source file"
                        validate={validate_255}
                    />
                    <TextInputWide
                        source="origin_cloud_qualified_resource"
                        label="Cloud qualified resource"
                        helperText="Regular expression to match the cloud qualified resource name"
                        validate={validate_255}
                    />
                    <TextInputWide
                        source="origin_kubernetes_qualified_resource"
                        label="Kubernetes qualified resource"
                        helperText="Regular expression to match the Kubernetes qualified resource name"
                        validate={validate_255}
                    />
                </Stack>
            </SimpleForm>
        </Create>
    );
};

export default GeneralRuleCreate;
