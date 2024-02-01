import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle, Divider, Stack, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    CreateBase,
    NumberInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    TextInput,
    Toolbar,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import {
    validate_255,
    validate_2048,
    validate_min_0_999999,
    validate_required,
    validate_required_255,
} from "../../commons/custom_validators";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES, OBSERVATION_STATUS_OPEN } from "../../core/types";

export type ObservationCreateProps = {
    id: any;
};

const ObservationCreate = ({ id }: ObservationCreateProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
            }}
            variant="contained"
            onClick={handleCancel}
            color="inherit"
            startIcon={<CancelIcon />}
        >
            Cancel
        </Button>
    );

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton />
            <SaveButton />
        </Toolbar>
    );

    const create_observation = (data: any) => {
        data.product = id;

        create(
            "observations",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Observation added", { type: "success" });
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
        setOpen(false);
    };

    return (
        <Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Add observation
            </Button>
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Add observation</DialogTitle>
                <DialogContent>
                    <CreateBase resource="observations">
                        <SimpleForm onSubmit={create_observation} toolbar={<CustomToolbar />}>
                            <Typography variant="h6">Observation</Typography>
                            <Stack>
                                <TextInputWide autoFocus source="title" validate={validate_required_255} />
                                <Stack direction="row" spacing={2}>
                                    <AutocompleteInputMedium
                                        source="parser_severity"
                                        label="Severity"
                                        choices={OBSERVATION_SEVERITY_CHOICES}
                                        validate={validate_required}
                                    />
                                    <AutocompleteInputMedium
                                        source="parser_status"
                                        label="Status"
                                        choices={OBSERVATION_STATUS_CHOICES}
                                        defaultValue={OBSERVATION_STATUS_OPEN}
                                        validate={validate_required}
                                    />
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
                                    sort={{ field: "name", order: "ASC" }}
                                >
                                    <AutocompleteInputWide optionText="name" defaultValue={id} disabled={true} />
                                </ReferenceInput>
                                <ReferenceInput
                                    source="branch"
                                    reference="branches"
                                    sort={{ field: "name", order: "ASC" }}
                                    filter={{ product: id }}
                                >
                                    <AutocompleteInputWide optionText="name" />
                                </ReferenceInput>
                            </Stack>

                            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                            <Typography variant="h6">Origins</Typography>
                            <Stack>
                                <TextInputWide
                                    source="origin_service_name"
                                    label="Service name"
                                    validate={validate_255}
                                />
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
                                        validate={validate_min_0_999999}
                                    />
                                    <NumberInput
                                        source="origin_source_line_end"
                                        label="Source line end"
                                        min={0}
                                        step={1}
                                        validate={validate_min_0_999999}
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
