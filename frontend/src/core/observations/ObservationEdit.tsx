import { Typography } from "@mui/material";
import {
    DeleteButton,
    Edit,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useRecordContext,
} from "react-admin";

import { PERMISSION_OBSERVATION_DELETE } from "../../access_control/types";
import { AutocompleteInputMedium, SelectInputWide, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../../core/types";

const CustomToolbar = () => {
    const observation = useRecordContext();

    return (
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
            <SaveButton />
            {observation && observation.product_data.permissions.includes(PERMISSION_OBSERVATION_DELETE) && (
                <DeleteButton mutationMode="pessimistic" />
            )}
        </Toolbar>
    );
};

const ObservationEdit = () => {
    const transform = (data: any) => {
        if (!data.description) {
            data.description = "";
        }
        if (!data.recommendation) {
            data.recommendation = "";
        }
        if (!data.origin_service_name) {
            data.origin_service_name = "";
        }
        if (!data.origin_component_name_version) {
            data.origin_component_name_version = "";
        }
        if (!data.origin_docker_image_name_tag) {
            data.origin_docker_image_name_tag = "";
        }
        if (!data.origin_endpoint_url) {
            data.origin_endpoint_url = "";
        }
        if (!data.origin_source_file) {
            data.origin_source_file = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }}>
                    <SelectInputWide optionText="name" disabled={true} />
                </ReferenceInput>
                <Typography variant="h6">Observation</Typography>
                <TextInputWide autoFocus source="title" validate={requiredValidate} />
                <AutocompleteInputMedium
                    source="parser_severity"
                    label="Severity"
                    choices={OBSERVATION_SEVERITY_CHOICES}
                    validate={requiredValidate}
                />
                <AutocompleteInputMedium
                    source="parser_status"
                    label="Status"
                    choices={OBSERVATION_STATUS_CHOICES}
                    validate={requiredValidate}
                />
                <TextInputWide source="description" multiline />
                <TextInputWide source="recommendation" multiline />
                <Typography variant="h6">Origins</Typography>
                <TextInputWide source="origin_service_name" label="Service name" />
                <TextInputWide source="origin_component_name_version" label="Component name:version" />
                <TextInputWide source="origin_docker_image_name_tag" label="Container name:tag" />
                <TextInputWide source="origin_endpoint_url" label="Endpoint URL" />
                <TextInputWide source="origin_source_file" label="Source file" />
                <NumberInput source="origin_source_line_start" label="Source line start" min={0} step={1} />
                <NumberInput source="origin_source_line_end" label="Source line end" min={0} step={1} />
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ObservationEdit;
