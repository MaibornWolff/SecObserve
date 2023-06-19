import CancelIcon from "@mui/icons-material/Cancel";
import UploadIcon from "@mui/icons-material/CloudUpload";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, required, useNotify, useRefresh } from "react-admin";

import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ApiImportObservations = (product: any) => {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => {
        setOpen(false);
        setLoading(false);
    };
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
        setLoading(false);
    };

    const observationUpdate = async (data: any) => {
        setLoading(true);

        const formData = new FormData();
        formData.append("api_configuration", data.api_configuration);
        if (data.branch) {
            formData.append("exsting_branch", data.branch);
        }
        formData.append("parser", data.parser);
        if (data.service) {
            formData.append("service", data.service);
        }
        if (data.docker_image_name_tag) {
            formData.append("docker_image_name_tag", data.docker_image_name_tag);
        }
        if (data.endpoint_url) {
            formData.append("endpoint_url", data.endpoint_url);
        }

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/import/api_import_observations_by_id/", {
            method: "POST",
            body: JSON.stringify(formData),
        })
            .then((result) => {
                const message =
                    result.json.observations_new +
                    " new observations\n" +
                    result.json.observations_updated +
                    " updated observations\n" +
                    result.json.observations_resolved +
                    " resolved observations";
                refresh();
                setLoading(false);
                setOpen(false);
                notify(message, {
                    type: "success",
                });
            })
            .catch((error) => {
                setLoading(false);
                setOpen(false);
                notify(error.message, {
                    type: "warning",
                });
            });
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
            <SaveButton label="Import" icon={<UploadIcon />} />
        </Toolbar>
    );

    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<UploadIcon />}
            >
                Import Observations From API
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Import Observations From API</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="api_configuration"
                            reference="api_configurations"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ product: product.product.id }}
                        >
                            <AutocompleteInputWide
                                optionText="name"
                                label="API configuration"
                                validate={requiredValidate}
                            />
                        </ReferenceInput>
                        <ReferenceInput
                            source="branch"
                            reference="branches"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ product: product.product.id }}
                            alwaysOn
                        >
                            <AutocompleteInputWide optionText="name" />
                        </ReferenceInput>
                        <TextInputWide source="service" />
                        <TextInputWide source="docker_image_name_tag" label="Docker image name:tag" />
                        <TextInputWide source="endpoint_url" />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
            {loading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </Fragment>
    );
};

const requiredValidate = [required()];

export default ApiImportObservations;
