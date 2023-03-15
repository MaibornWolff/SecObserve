import * as React from "react";
import {
    SimpleForm,
    ReferenceInput,
    required,
    useCreate,
    useRefresh,
    useNotify,
    CreateBase,
    Toolbar,
    SaveButton,
    NumberInput,
} from "react-admin";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    Button,
    Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import {
    TextInputWide,
    SelectInputWide,
    AutocompleteInputMedium,
} from "../../commons/layout/themes";
import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
} from "../../core/types";

export type ObservationCreateProps = {
    id: any;
};

const ObservationCreate = ({ id }: ObservationCreateProps) => {
    const [open, setOpen] = React.useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const [create] = useCreate();

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
                color: "#000000dd",
            }}
            variant="contained"
            onClick={handleClose}
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
        <React.Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Add observation
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add observation</DialogTitle>
                <DialogContent>
                    <CreateBase resource="observations">
                        <SimpleForm
                            onSubmit={create_observation}
                            toolbar={<CustomToolbar />}
                        >
                            <ReferenceInput
                                source="product"
                                reference="products"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <SelectInputWide
                                    optionText="name"
                                    defaultValue={id}
                                    disabled={true}
                                />
                            </ReferenceInput>
                            <Typography variant="h6">Observation</Typography>
                            <TextInputWide
                                autoFocus
                                source="title"
                                validate={requiredValidate}
                            />
                            <AutocompleteInputMedium
                                source="current_severity"
                                label="Severity"
                                choices={OBSERVATION_SEVERITY_CHOICES}
                                validate={requiredValidate}
                            />
                            <AutocompleteInputMedium
                                source="current_status"
                                label="Status"
                                choices={OBSERVATION_STATUS_CHOICES}
                                defaultValue={OBSERVATION_STATUS_OPEN}
                                validate={requiredValidate}
                            />
                            <TextInputWide source="description" multiline />
                            <TextInputWide source="recommendation" multiline />
                            <Typography variant="h6">Origins</Typography>
                            <TextInputWide
                                source="origin_service_name"
                                label="Service name"
                            />
                            <TextInputWide
                                source="origin_component_name_version"
                                label="Component name:version"
                            />
                            <TextInputWide
                                source="origin_docker_image_name_tag"
                                label="Container name:tag"
                            />
                            <TextInputWide
                                source="origin_endpoint_url"
                                label="Endpoint URL"
                            />
                            <TextInputWide
                                source="origin_source_file"
                                label="Source file"
                            />
                            <NumberInput
                                source="origin_source_line_start"
                                label="Source line start"
                                min={0}
                                step={1}
                            />
                            <NumberInput
                                source="origin_source_line_end"
                                label="Source line end"
                                min={0}
                                step={1}
                            />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ObservationCreate;
