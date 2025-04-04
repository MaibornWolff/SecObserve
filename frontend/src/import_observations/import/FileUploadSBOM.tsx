import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    FileField,
    FileInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    WithRecord,
    useNotify,
    useRefresh,
} from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import MenuButton from "../../commons/custom_fields/MenuButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_required } from "../../commons/custom_validators";
import { getIconAndFontColor } from "../../commons/functions";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

interface CustomToolbarProps {
    handleCancel: () => void;
}

const CustomToolbar = ({ handleCancel }: CustomToolbarProps) => (
    <Toolbar>
        <CancelButton onClick={handleCancel} />
        <SaveButton label="Upload" icon={<UploadIcon />} />
    </Toolbar>
);

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

        const formData = new FormData();
        formData.append("file", data.file.rawFile, data.file.title);
        formData.append("product", data.id);
        if (data.branch) {
            formData.append("branch", data.branch);
        }

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/import/file_upload_sbom_by_id/", {
            method: "POST",
            body: formData,
        })
            .then((result) => {
                const message =
                    result.json.license_components_new +
                    " new license components\n" +
                    result.json.license_components_updated +
                    " updated license components\n" +
                    result.json.license_components_deleted +
                    " deleted license components";
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
                title="Upload SBOM from file"
                onClick={handleOpen}
                icon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            />
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Upload SBOM from file</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={uploadSBOM} toolbar={<CustomToolbar handleCancel={handleCancel} />}>
                        <FileInput
                            source="file"
                            label="SBOM"
                            accept={{ "application/octet-stream": [".json"] }}
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
