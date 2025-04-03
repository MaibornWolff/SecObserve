import { Divider, Stack, Typography } from "@mui/material";
import { useState } from "react";
import {
    BooleanInput,
    DeleteButton,
    Edit,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useRecordContext,
} from "react-admin";

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
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../../core/types";
import { non_duplicate_transform, validateRuleForm } from "../functions";

const CustomToolbar = () => {
    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            <DeleteButton mutationMode="pessimistic" />
        </Toolbar>
    );
};
const GeneralRuleEdit = () => {
    const transform = (data: any) => {
        data = non_duplicate_transform(data);
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <GeneralRuleEditForm />
        </Edit>
    );
};
const GeneralRuleEditForm = () => {
    const generalRule = useRecordContext();
    const [status, setStatus] = useState(generalRule ? generalRule.new_status : "");
    const justificationEnabled = justificationIsEnabledForStatus(status);

    return (
        <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />} validate={validateRuleForm}>
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
    );
};

export default GeneralRuleEdit;
