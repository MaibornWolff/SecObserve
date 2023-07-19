import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import {
    BooleanInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useNotify,
    useRefresh,
    useUpdate,
} from "react-admin";

import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../../core/types";

const ProductRuleEdit = () => {
    const [open, setOpen] = React.useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const product_rule_update = async (data: any) => {
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

        const patch = {
            name: data.name,
            parser: data.parser,
            scanner_prefix: data.scanner_prefix,
            title: data.title,
            origin_component_name_version: data.origin_component_name_version,
            origin_docker_image_name_tag: data.origin_docker_image_name_tag,
            origin_endpoint_url: data.origin_endpoint_url,
            origin_service_name: data.origin_service_name,
            origin_source_file: data.origin_source_file,
            new_severity: data.new_severity,
            new_status: data.new_status,
            enabled: data.enabled,
        };

        update(
            "product_rules",
            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("Product rule updated", {
                        type: "success",
                    });
                },
                onError: (error: any) => {
                    notify(error.message, {
                        type: "warning",
                    });
                },
            }
        );
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
    return (
        <React.Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<EditIcon />}
            >
                Edit
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit product rule</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={product_rule_update} toolbar={<CustomToolbar />}>
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
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ProductRuleEdit;
