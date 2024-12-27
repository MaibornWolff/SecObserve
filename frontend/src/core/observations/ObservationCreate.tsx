import { Dialog, DialogContent, DialogTitle, Divider, Stack, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    CreateBase,
    DateInput,
    FormDataConsumer,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    TextInput,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import AddButton from "../../commons/custom_fields/AddButton";
import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
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
    OBSERVATION_STATUS_OPEN,
    OBSERVATION_STATUS_RISK_ACCEPTED,
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../../core/types";

export type ObservationCreateProps = {
    id: any;
    risk_acceptance_expiry_date_calculated: any;
};

const ObservationCreate = ({ id, risk_acceptance_expiry_date_calculated }: ObservationCreateProps) => {
    const [open, setOpen] = useState(false);
    const [status, setStatus] = useState(OBSERVATION_STATUS_OPEN);
    const justificationEnabled = justificationIsEnabledForStatus(status);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    const create_observation = (data: any) => {
        data.product = id;
        if (!justificationEnabled) {
            data.parser_vex_justification = "";
        }
        if (data.parser_status != OBSERVATION_STATUS_RISK_ACCEPTED) {
            data.risk_acceptance_expiry_date = null;
        }

        create(
            "observations",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Observation added", { type: "success" });
                    setOpen(false);
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
    };

    return (
        <Fragment>
            <AddButton title="Add observation" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Add observation</DialogTitle>
                <DialogContent>
                    <CreateBase resource="observations">
                        <SimpleForm onSubmit={create_observation} toolbar={<CustomToolbar />}>
                            <Typography variant="h6">Observation</Typography>
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
                                        defaultValue={OBSERVATION_STATUS_OPEN}
                                        onChange={(e) => setStatus(e)}
                                        validate={validate_required}
                                    />
                                    <FormDataConsumer>
                                        {({ formData }) =>
                                            formData.parser_status &&
                                            formData.parser_status == OBSERVATION_STATUS_RISK_ACCEPTED &&
                                            risk_acceptance_expiry_date_calculated && (
                                                <DateInput
                                                    source="risk_acceptance_expiry_date"
                                                    label="Risk acceptance expiry date"
                                                    defaultValue={risk_acceptance_expiry_date_calculated}
                                                    validate={validate_after_today()}
                                                />
                                            )
                                        }
                                    </FormDataConsumer>
                                    {justificationEnabled && (
                                        <AutocompleteInputMedium
                                            source="parser_vex_justification"
                                            label="VEX Justification"
                                            choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                                        />
                                    )}
                                </Stack>
                                <TextInputWide
                                    source="description"
                                    multiline
                                    minRows={3}
                                    validate={validate_2048}
                                    helperText="Markdown is supported when showing the observation"
                                />
                                <TextInputWide
                                    source="recommendation"
                                    multiline
                                    minRows={3}
                                    validate={validate_2048}
                                    helperText="Markdown is supported when showing the observation"
                                />
                            </Stack>

                            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                            <Typography variant="h6">Product</Typography>
                            <Stack>
                                <ReferenceInput
                                    source="product"
                                    reference="products"
                                    queryOptions={{ meta: { api_resource: "product_names" } }}
                                    sort={{ field: "name", order: "ASC" }}
                                >
                                    <AutocompleteInputWide optionText="name" defaultValue={id} disabled={true} />
                                </ReferenceInput>
                                <ReferenceInput
                                    source="branch"
                                    reference="branches"
                                    queryOptions={{ meta: { api_resource: "branch_names" } }}
                                    sort={{ field: "name", order: "ASC" }}
                                    filter={{ product: id }}
                                >
                                    <AutocompleteInputWide optionText="name" label="Branch / Version" />
                                </ReferenceInput>
                            </Stack>

                            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                            <Typography variant="h6">Vulnerability</Typography>
                            <Stack>
                                <TextInputWide
                                    source="vulnerability_id"
                                    label="Vulnerability ID"
                                    validate={validate_255}
                                />
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

                            <Typography variant="h6">Origins</Typography>
                            <Stack>
                                <ReferenceInput
                                    source="origin_service"
                                    reference="services"
                                    sort={{ field: "name", order: "ASC" }}
                                    filter={{ product: id }}
                                >
                                    <AutocompleteInputWide optionText="name" label="Service" />
                                </ReferenceInput>
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_component_name"
                                        label="Component name"
                                        validate={validate_255}
                                    />
                                    <TextInput
                                        source="origin_component_version"
                                        label="Component version"
                                        validate={validate_255}
                                    />
                                </Stack>
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_docker_image_name"
                                        label="Container name"
                                        validate={validate_255}
                                    />
                                    <TextInput
                                        source="origin_docker_image_tag"
                                        label="Container tag"
                                        validate={validate_255}
                                    />
                                </Stack>
                                <TextInputWide
                                    source="origin_endpoint_url"
                                    label="Endpoint URL"
                                    validate={validate_2048}
                                />
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_source_file"
                                        label="Source file"
                                        validate={validate_255}
                                    />
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
                                    <TextInputWide
                                        source="origin_cloud_provider"
                                        label="Cloud provider"
                                        validate={validate_255}
                                    />
                                    <TextInputWide
                                        source="origin_cloud_account_subscription_project"
                                        label="Account / Subscription / Project"
                                        validate={validate_255}
                                    />
                                </Stack>
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_cloud_resource_type"
                                        label="Cloud resource type"
                                        validate={validate_255}
                                    />
                                    <TextInputWide
                                        source="origin_cloud_resource"
                                        label="Cloud resource"
                                        validate={validate_255}
                                    />
                                </Stack>
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_kubernetes_cluster"
                                        label="Kubernetes cluster"
                                        validate={validate_255}
                                    />
                                    <TextInputWide
                                        source="origin_kubernetes_namespace"
                                        label="Namespace"
                                        validate={validate_255}
                                    />
                                </Stack>
                                <Stack direction="row" spacing={2}>
                                    <TextInputWide
                                        source="origin_kubernetes_resource_type"
                                        label="Kubernetes resource type"
                                        validate={validate_255}
                                    />
                                    <TextInputWide
                                        source="origin_kubernetes_resource_name"
                                        label="Kubernetes resource name"
                                        validate={validate_255}
                                    />
                                </Stack>
                            </Stack>
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ObservationCreate;
