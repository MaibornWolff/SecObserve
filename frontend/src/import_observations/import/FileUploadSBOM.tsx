import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { FileField, FileInput, ReferenceInput, SimpleForm, WithRecord, useNotify, useRefresh } from "react-admin";

import MenuButton from "../../commons/custom_fields/MenuButton";
import { ToolbarCancelSave } from "../../commons/custom_fields/ToolbarCancelSave";
import { validate_required } from "../../commons/custom_validators";
import { getIconAndFontColor } from "../../commons/functions";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const FileUploadSBOM = () => {
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

    const uploadSBOM = async (data: any) => {
        setLoading(true);

        let new_license_components = 0;
        let updated_license_components = 0;
        let deleted_license_components = 0;

        let upload_error = false;
        let error_message = "";
        let error_sbom = "";

        for (const file of data.file) {
            const formData = new FormData();
            formData.append("file", file.rawFile, file.title);
            formData.append("product", data.id);
            if (data.branch) {
                formData.append("branch", data.branch);
            }
            if (data.service_id) {
                formData.append("service_id", data.service_id);
            }

            await httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/import/file_upload_sbom_by_id/", {
                method: "POST",
                body: formData,
            })
                .then((result) => {
                    new_license_components += result.json.license_components_new;
                    updated_license_components += result.json.license_components_updated;
                    deleted_license_components += result.json.license_components_deleted;
                })
                .catch((error) => {
                    upload_error = true;
                    error_message = error.message;
                    error_sbom = file.title;
                });

            if (upload_error) {
                break;
            }
        }

        setLoading(false);
        setOpen(false);
        refresh();

        if (upload_error) {
            notify("Error '" + error_message + "' while processing '" + error_sbom + "'", { type: "warning" });
        } else {
            const message =
                new_license_components +
                " new license components\n" +
                updated_license_components +
                " updated license components\n" +
                deleted_license_components +
                " deleted license components";
            notify(message, {
                type: "success",
                multiLine: true,
            });
        }
    };

    return (
        <Fragment>
            <MenuButton
                title="Upload SBOMs from files"
                onClick={handleOpen}
                icon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            />
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Upload SBOMs from files</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={uploadSBOM}
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
                            label="SBOMs (max 10 files)"
                            accept={{ "application/octet-stream": [".json"] }}
                            validate={validate_required}
                            multiple={true}
                            options={{ maxFiles: 10 }}
                            placeholder={<p>Drop some files to upload, or click to select some.</p>}
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
                                    {product.has_services && (
                                        <ReferenceInput
                                            source="service_id"
                                            reference="services"
                                            sort={{ field: "name", order: "ASC" }}
                                            queryOptions={{ meta: { api_resource: "service_names" } }}
                                            filter={{ product: product.id }}
                                            alwaysOn
                                        >
                                            <AutocompleteInputWide optionText="name" label="Service" />
                                        </ReferenceInput>
                                    )}
                                </Fragment>
                            )}
                        />
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

export default FileUploadSBOM;
