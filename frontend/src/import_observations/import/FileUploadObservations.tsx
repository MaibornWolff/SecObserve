import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { FileField, FileInput, ReferenceInput, SimpleForm, WithRecord, useNotify, useRefresh } from "react-admin";

import MenuButton from "../../commons/custom_fields/MenuButton";
import { ToolbarCancelSave } from "../../commons/custom_fields/ToolbarCancelSave";
import { validate_255, validate_513, validate_2048, validate_required } from "../../commons/custom_validators";
import { getIconAndFontColor } from "../../commons/functions";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const FileUploadObservations = () => {
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
        formData.append("file", data.file.rawFile, data.file.title);
        formData.append("product", data.id);
        if (data.branch) {
            formData.append("branch", data.branch);
        }
        if (data.service) {
            formData.append("service", data.service);
        }
        if (data.docker_image_name_tag) {
            formData.append("docker_image_name_tag", data.docker_image_name_tag);
        }
        if (data.endpoint_url) {
            formData.append("endpoint_url", data.endpoint_url);
        }
        if (data.kubernetes_cluster) {
            formData.append("kubernetes_cluster", data.kubernetes_cluster);
        }
        formData.append("suppress_licenses", "true");

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/import/file_upload_observations_by_id/", {
            method: "POST",
            body: formData,
        })
            .then((result) => {
                const observations =
                    result.json.observations_new +
                        result.json.observations_updated +
                        result.json.observations_resolved >
                    0;
                const license_components =
                    result.json.license_components_new +
                        result.json.license_components_updated +
                        result.json.license_components_deleted >
                    0;
                let message = "";
                if (observations || !license_components)
                    message +=
                        result.json.observations_new +
                        " new observations\n" +
                        result.json.observations_updated +
                        " updated observations\n" +
                        result.json.observations_resolved +
                        " resolved observations";
                if (observations && license_components) message += "\n";
                if (license_components) {
                    message +=
                        result.json.license_components_new +
                        " new license components\n" +
                        result.json.license_components_updated +
                        " updated license components\n" +
                        result.json.license_components_deleted +
                        " deleted license components";
                }
                refresh();
                setLoading(false);
                setOpen(false);
                notify(message, {
                    type: "success",
                    multiLine: true,
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

    return (
        <Fragment>
            <MenuButton
                title="Upload observations from file"
                onClick={handleOpen}
                icon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            />
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Upload observations from file</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={observationUpdate}
                        toolbar={
                            <ToolbarCancelSave
                                onClick={handleCancel}
                                saveButtonLabel="Upload"
                                saveButtonIcon={<UploadIcon />}
                            />
                        }
                    >
                        <FileInput
                            source="file"
                            label="Scan report"
                            accept={{ "application/octet-stream": [".csv, .json, .sarif"] }}
                            validate={validate_required}
                        >
                            <FileField source="src" title="title" />
                        </FileInput>
                        <WithRecord
                            render={(product) => (
                                <Fragment>
                                    {product.has_branches && (
                                        <ReferenceInput
                                            source="branch"
                                            reference="branches"
                                            sort={{ field: "name", order: "ASC" }}
                                            queryOptions={{ meta: { api_resource: "branch_names" } }}
                                            filter={{ product: product.id }}
                                            alwaysOn
                                        >
                                            <AutocompleteInputWide
                                                optionText="name"
                                                label="Branch / Version"
                                                defaultValue={product.repository_default_branch}
                                            />
                                        </ReferenceInput>
                                    )}
                                </Fragment>
                            )}
                        />
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

export default FileUploadObservations;
