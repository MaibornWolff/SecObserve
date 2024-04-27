import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle, Divider, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    BooleanInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useNotify,
    useRecordContext,
    useRefresh,
    useUpdate,
} from "react-admin";

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
import { validateRuleForm } from "../functions";

const ProductRuleEdit = () => {
    const [open, setOpen] = useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const productRule = useRecordContext();
    const [status, setStatus] = useState(productRule.new_status);
    const justificationEnabled = justificationIsEnabledForStatus(status);

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
        if (!justificationEnabled || data.new_vex_justification == null) {
            data.new_vex_justification = "";
        }

        const patch = {
            name: data.name,
            description: data.description,
            parser: data.parser,
            scanner_prefix: data.scanner_prefix,
            title: data.title,
            description_observation: data.description_observation,
            origin_component_name_version: data.origin_component_name_version,
            origin_docker_image_name_tag: data.origin_docker_image_name_tag,
            origin_endpoint_url: data.origin_endpoint_url,
            origin_service_name: data.origin_service_name,
            origin_source_file: data.origin_source_file,
            origin_cloud_qualified_resource: data.origin_cloud_qualified_resource,
            new_severity: data.new_severity,
            new_status: data.new_status,
            new_vex_justification: data.new_vex_justification,
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
        <Fragment>
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
                    <SimpleForm onSubmit={product_rule_update} toolbar={<CustomToolbar />} validate={validateRuleForm}>
                        <Typography variant="h6">Rule</Typography>
                        <TextInputWide autoFocus source="name" validate={validate_required_255} />
                        <TextInputWide
                            source="description"
                            multiline
                            minRows={3}
                            validate={validate_required_2048}
                            helperText="Markdown supported. Description will be copied into the Observation Log."
                        />
                        <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                        <AutocompleteInputMedium
                            source="new_status"
                            choices={OBSERVATION_STATUS_CHOICES}
                            onChange={(e) => setStatus(e)}
                        />
                        {justificationEnabled && (
                            <AutocompleteInputMedium
                                source="new_vex_justification"
                                choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                            />
                        )}
                        <BooleanInput source="enabled" />

                        <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                        <Typography variant="h6">Observation</Typography>
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

                        <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                        <Typography variant="h6">Origins</Typography>
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
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductRuleEdit;
