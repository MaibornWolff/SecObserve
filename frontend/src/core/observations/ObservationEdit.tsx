import { Divider, Stack, Typography } from "@mui/material";
import { useState } from "react";
import {
    DateInput,
    DeleteButton,
    Edit,
    FormDataConsumer,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    TextInput,
    Toolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { PERMISSION_OBSERVATION_DELETE } from "../../access_control/types";
import {
    validate_0_10,
    validate_0_999999,
    validate_255,
    validate_2048,
    validate_after_today,
    validate_required,
    validate_required_255,
} from "../../commons/custom_validators";
import { justificationIsEnabledForStatus } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_RISK_ACCEPTED,
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../../core/types";

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

const ObservationEditForm = () => {
    const observation = useRecordContext();
    const [status, setStatus] = useState(observation ? observation.parser_status : "");
    const justificationEnabled = justificationIsEnabledForStatus(status);

    return (
        <SimpleForm warnWhenUnsavedChanges toolbar={<CustomToolbar />}>
            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Observation
            </Typography>
            <Stack>
                <TextInputWide autoFocus source="title" validate={validate_required_255} />
                <Stack direction="row" spacing={2} alignItems="center">
                    <AutocompleteInputMedium
                        source="parser_severity"
                        label="Severity"
                        choices={OBSERVATION_SEVERITY_CHOICES}
                    />
                    <AutocompleteInputMedium
                        source="parser_status"
                        label="Status"
                        choices={OBSERVATION_STATUS_CHOICES}
                        validate={validate_required}
                        onChange={(e) => setStatus(e)}
                    />
                    <FormDataConsumer>
                        {({ formData }) =>
                            formData.parser_status &&
                            formData.parser_status == OBSERVATION_STATUS_RISK_ACCEPTED &&
                            formData.product_data.risk_acceptance_expiry_date_calculated && (
                                <DateInput
                                    source="risk_acceptance_expiry_date"
                                    label="Risk acceptance expiry date"
                                    defaultValue={formData.product_data.risk_acceptance_expiry_date_calculated}
                                    validate={validate_after_today()}
                                />
                            )
                        }
                    </FormDataConsumer>
                    {justificationEnabled && (
                        <AutocompleteInputMedium
                            source="parser_vex_justification"
                            label="VEX justification"
                            choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                        />
                    )}
                </Stack>
                <TextInputWide
                    source="description"
                    multiline
                    minRows={3}
                    helperText="Markdown is supported when showing the observation"
                    validate={validate_2048}
                />
                <TextInputWide
                    source="recommendation"
                    multiline
                    minRows={3}
                    helperText="Markdown is supported when showing the observation"
                    validate={validate_2048}
                />
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Product
            </Typography>
            <Stack>
                <TextInputWide source="product_data.name" label="Product" disabled />
                <WithRecord
                    render={(branch) => (
                        <ReferenceInput
                            source="branch"
                            reference="branches"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ product: branch.product_data.id }}
                        >
                            <AutocompleteInputWide optionText="name" label="Branch / Version" />
                        </ReferenceInput>
                    )}
                />
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6">Vulnerability</Typography>
            <Stack>
                <TextInputWide source="vulnerability_id" label="Vulnerability ID" validate={validate_255} />
                <Stack direction="row" spacing={2}>
                    <NumberInput
                        source="cvss3_score"
                        label="CVSS3 score"
                        min={0}
                        step={0.1}
                        validate={validate_0_10}
                        sx={{ width: "10em" }}
                    />
                    <TextInputWide source="cvss3_vector" label="CVSS3 vector" validate={validate_255} />
                </Stack>
                <NumberInput
                    source="cwe"
                    label="CWE"
                    min={0}
                    step={1}
                    validate={validate_0_999999}
                    sx={{ width: "10em" }}
                />
            </Stack>

            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6" sx={{ marginBottom: 2 }}>
                Origins
            </Typography>
            <Stack>
                <TextInputWide source="origin_service_name" label="Service name" validate={validate_255} />
                <Stack direction="row" spacing={2}>
                    <TextInputWide source="origin_component_name" label="Component name" validate={validate_255} />
                    <TextInput source="origin_component_version" label="Component version" validate={validate_255} />
                </Stack>
                <Stack direction="row" spacing={2}>
                    <TextInputWide source="origin_docker_image_name" label="Container name" validate={validate_255} />
                    <TextInput source="origin_docker_image_tag" label="Container tag" validate={validate_255} />
                </Stack>
                <TextInputWide source="origin_endpoint_url" label="Endpoint URL" validate={validate_2048} />
                <Stack direction="row" spacing={2}>
                    <TextInputWide source="origin_source_file" label="Source file" validate={validate_255} />
                    <NumberInput
                        source="origin_source_line_start"
                        label="Source line start"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                    />
                    <NumberInput
                        source="origin_source_line_end"
                        label="Source line end"
                        min={0}
                        step={1}
                        validate={validate_0_999999}
                    />
                </Stack>
                <Stack direction="row" spacing={2}>
                    <TextInputWide source="origin_cloud_provider" label="Cloud provider" validate={validate_255} />
                    <TextInputWide
                        source="origin_cloud_account_subscription_project"
                        label="Account / Subscription / Project"
                        validate={validate_255}
                    />
                </Stack>
                <Stack direction="row" spacing={2}>
                    <TextInputWide source="origin_cloud_resource" label="Cloud resource" validate={validate_255} />
                    <TextInputWide source="origin_cloud_resource_type" label="Resource type" validate={validate_255} />
                </Stack>
            </Stack>
        </SimpleForm>
    );
};

const ObservationEdit = () => {
    const transform = (data: any) => {
        if (!data.parser_severity) {
            data.parser_severity = "";
        }
        if (!data.description) {
            data.description = "";
        }
        if (!data.recommendation) {
            data.recommendation = "";
        }
        if (!data.origin_service_name) {
            data.origin_service_name = "";
        }
        if (!data.origin_component_name) {
            data.origin_component_name = "";
        }
        if (!data.origin_component_version) {
            data.origin_component_version = "";
        }
        if (!data.origin_docker_image_name) {
            data.origin_docker_image_name = "";
        }
        if (!data.origin_docker_image_tag) {
            data.origin_docker_image_tag = "";
        }
        if (!data.origin_endpoint_url) {
            data.origin_endpoint_url = "";
        }
        if (!data.origin_source_file) {
            data.origin_source_file = "";
        }
        if (!data.origin_cloud_provider) {
            data.origin_cloud_provider = "";
        }
        if (!data.origin_cloud_account_subscription_project) {
            data.origin_cloud_account_subscription_project = "";
        }
        if (!data.origin_cloud_resource) {
            data.origin_cloud_resource = "";
        }
        if (!data.origin_cloud_resource_type) {
            data.origin_cloud_resource_type = "";
        }
        if (!data.origin_cloud_provider) {
            data.origin_cloud_provider = "";
        }
        if (!justificationIsEnabledForStatus(data.parser_status) || !data.parser_vex_justification) {
            data.parser_vex_justification = "";
        }
        if (data.parser_status != OBSERVATION_STATUS_RISK_ACCEPTED) {
            data.risk_acceptance_expiry_date = null;
        }
        data.origin_component_name_version = "";
        data.origin_docker_image_name_tag = "";
        if (!data.vulnerability_id) {
            data.vulnerability_id = "";
        }
        if (!data.cvss3_vector) {
            data.cvss3_vector = "";
        }
        return data;
    };

    return (
        <Edit redirect="show" mutationMode="pessimistic" transform={transform}>
            <ObservationEditForm />
        </Edit>
    );
};

export default ObservationEdit;
