import UploadIcon from "@mui/icons-material/CloudUpload";
import { Backdrop, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import MenuButton from "../../commons/custom_fields/MenuButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_255, validate_513, validate_2048, validate_required } from "../../commons/custom_validators";
import { getIconAndFontColor } from "../../commons/functions";
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

        const formData: any = {
            api_configuration: data.api_configuration,
            parser: data.parser,
        };
        if (data.branch) {
            formData.branch = data.branch;
        }
        if (data.service) {
            formData.service = data.service;
        }
        if (data.docker_image_name_tag) {
            formData.docker_image_name_tag = data.docker_image_name_tag;
        }
        if (data.endpoint_url) {
            formData.endpoint_url = data.endpoint_url;
        }
        if (data.kubernetes_cluster) {
            formData.kubernetes_cluster = data.kubernetes_cluster;
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

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Import" icon={<UploadIcon />} />
        </Toolbar>
    );

    return (
        <Fragment>
            <MenuButton
                title="Import observations from API"
                onClick={handleOpen}
                icon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            />
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Import observations from API</DialogTitle>
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
                                validate={validate_required}
                            />
                        </ReferenceInput>
                        {product.product.has_branches && (
                            <ReferenceInput
                                source="branch"
                                reference="branches"
                                queryOptions={{ meta: { api_resource: "branch_names" } }}
                                sort={{ field: "name", order: "ASC" }}
                                filter={{ product: product.product.id }}
                                alwaysOn
                            >
                                <AutocompleteInputWide
                                    optionText="name"
                                    label="Branch / Version"
                                    defaultValue={product.product.repository_default_branch}
                                />
                            </ReferenceInput>
                        )}
                        <TextInputWide source="service" validate={validate_255} />
                        <TextInputWide
                            source="docker_image_name_tag"
                            label="Docker image name:tag"
                            validate={validate_513}
                        />
                        <TextInputWide label="Endpoint URL" source="endpoint_url" validate={validate_2048} />
                        <TextInputWide source="kubernetes_cluster" validate={validate_255} />
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

export default ApiImportObservations;
