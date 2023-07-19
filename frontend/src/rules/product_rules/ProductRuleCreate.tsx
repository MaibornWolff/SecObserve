import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../../core/types";

export type ProductRuleCreateProps = {
    id: any;
};

const ProductRuleCreate = ({ id }: ProductRuleCreateProps) => {
    const [open, setOpen] = React.useState(false);
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
                color: "#000000dd",
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

    const create_product_rule = (data: any) => {
        data.product = id;

        if (data.scanner_prefix == null) {
            data.scanner_prefix = "";
        }
        if (data.title == null) {
            data.title = "";
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
        if (data.new_severity == null) {
            data.new_severity = "";
        }
        if (data.new_status == null) {
            data.new_status = "";
        }

        create(
            "product_rules",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Product rule added", { type: "success" });
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
                Add product rule
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add product rule</DialogTitle>
                <DialogContent>
                    <CreateBase resource="product_rules">
                        <SimpleForm onSubmit={create_product_rule} toolbar={<CustomToolbar />}>
                            <TextInputWide autoFocus source="name" validate={requiredValidate} />
                            <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }}>
                                <AutocompleteInputWide optionText="name" validate={requiredValidate} />
                            </ReferenceInput>
                            <TextInputWide source="scanner_prefix" />
                            <TextInputWide
                                source="title"
                                label="Observation title"
                                helperText="Regular expression to match the observation's title"
                            />
                            <TextInputWide
                                source="origin_component_name_version"
                                label="Origin component name:version"
                                helperText="Regular expression to match the component name:version"
                            />
                            <TextInputWide
                                source="origin_docker_image_name_tag"
                                label="Origin docker image name:tag"
                                helperText="Regular expression to match the docker image name:tag"
                            />
                            <TextInputWide
                                source="origin_endpoint_url"
                                label="Origin endpoint URL"
                                helperText="Regular expression to match the endpoint URL"
                            />
                            <TextInputWide
                                source="origin_service_name"
                                label="Origin service name"
                                helperText="Regular expression to match the service name"
                            />
                            <TextInputWide
                                source="origin_source_file"
                                label="Origin source file"
                                helperText="Regular expression to match the source file"
                            />
                            <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                            <AutocompleteInputMedium source="new_status" choices={OBSERVATION_STATUS_CHOICES} />
                            <BooleanInput source="enabled" defaultValue={true} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ProductRuleCreate;
