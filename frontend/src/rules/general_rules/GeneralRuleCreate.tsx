import { Divider, Stack, Typography } from "@mui/material";
import { RichTextInput } from "ra-input-rich-text";
import { BooleanInput, Create, ReferenceInput, SimpleForm } from "react-admin";

import { validate_255, validate_513, validate_2048, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../../core/types";
import { validateRuleForm } from "../functions";

const transform = (data: any) => {
    if (data.description == null) {
        data.description = "";
    }
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
    if (data.new_severity == null) {
        data.new_severity = "";
    }
    if (data.new_status == null) {
        data.new_status = "";
    }
    return data;
};

const GeneralRuleCreate = () => {
    return (
        <Create redirect="show" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges validate={validateRuleForm}>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Rule
                </Typography>
                <Stack>
                    <TextInputWide autoFocus source="name" validate={validate_required_255} />
                    <RichTextInput source="description" validate={validate_2048} />
                    <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                    <AutocompleteInputMedium source="new_status" choices={OBSERVATION_STATUS_CHOICES} />
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
                        helperText="Regular expression to match the qualified resource name"
                        validate={validate_255}
                    />
                </Stack>
            </SimpleForm>
        </Create>
    );
};

export default GeneralRuleCreate;
