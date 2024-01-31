import { Divider, Stack, Typography } from "@mui/material";
import {
    DeleteButton,
    Edit,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    TextInput,
    Toolbar,
    WithRecord,
    required,
    useRecordContext,
} from "react-admin";

import { PERMISSION_OBSERVATION_DELETE } from "../../access_control/types";
import {
    AutocompleteInputMedium,
    AutocompleteInputWide,
    SelectInputWide,
    TextInputWide,
} from "../../commons/layout/themes";
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
        data.origin_component_name_version = "";
        data.origin_docker_image_name_tag = "";
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Observation
                </Typography>
                <Stack>
                    <TextInputWide autoFocus source="title" validate={requiredValidate} />
                    <Stack direction="row" spacing={2}>
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
                    </Stack>
                    <TextInputWide source="description" multiline />
                    <TextInputWide source="recommendation" multiline />
                </Stack>

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Product
                </Typography>
                <Stack>
                    <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }}>
                        <SelectInputWide optionText="name" disabled={true} />
                    </ReferenceInput>
                    <WithRecord
                        render={(branch) => (
                            <ReferenceInput
                                source="branch"
                                reference="branches"
                                sort={{ field: "name", order: "ASC" }}
                                filter={{ product: branch.product_data.id }}
                            >
                                <AutocompleteInputWide optionText="name" />
                            </ReferenceInput>
                        )}
                    />
                </Stack>

                <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                <Typography variant="h6" sx={{ marginBottom: 2 }}>
                    Origins
                </Typography>
                <Stack>
                    <TextInputWide source="origin_service_name" label="Service name" />
                    <Stack direction="row" spacing={2}>
                        <TextInputWide source="origin_component_name" label="Component name" />
                        <TextInput source="origin_component_version" label="Component version" />
                    </Stack>
                    <Stack direction="row" spacing={2}>
                        <TextInputWide source="origin_docker_image_name" label="Container name" />
                        <TextInput source="origin_docker_image_tag" label="Container tag" />
                    </Stack>
                    <TextInputWide source="origin_endpoint_url" label="Endpoint URL" />
                    <Stack direction="row" spacing={2}>
                        <TextInputWide source="origin_source_file" label="Source file" />
                        <NumberInput source="origin_source_line_start" label="Source line start" min={0} step={1} />
                        <NumberInput source="origin_source_line_end" label="Source line end" min={0} step={1} />
                    </Stack>
                    <Stack direction="row" spacing={2}>
                        <TextInputWide source="origin_cloud_provider" label="Cloud provider" />
                        <TextInputWide
                            source="origin_cloud_account_subscription_project"
                            label="Account / Subscription / Project"
                        />
                    </Stack>
                    <Stack direction="row" spacing={2}>
                        <TextInputWide source="origin_cloud_resource" label="Cloud resource" />
                        <TextInputWide source="origin_cloud_resource_type" label="Resource type" />
                    </Stack>
                </Stack>
            </SimpleForm>
        </Edit>
    );
};

const requiredValidate = [required()];

export default ObservationEdit;
