import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { ChangeEvent, Fragment, useState } from "react";
import {
    BooleanInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    WithRecord,
    useNotify,
    useRefresh,
} from "react-admin";
import { makeStyles } from "tss-react/mui";

import CancelButton from "../../commons/custom_fields/CancelButton";
import { validate_255, validate_513, validate_2048, validate_required } from "../../commons/custom_validators";
import { getIconAndFontColor } from "../../commons/functions";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const FileUploadObservations = () => {
    const useStyles = makeStyles()({
        input: {
            marginTop: "2em",
            marginBottom: "2em",
        },
    });

    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [fileSelected, setFileSelected] = useState<File>();
    const { classes } = useStyles();
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

    const handleFileChange = function (e: ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files;
        if (!fileList) return;
        setFileSelected(fileList[0]);
    };

    const observationUpdate = async (data: any) => {
        if (fileSelected) {
            setLoading(true);

            const formData = new FormData();
            formData.append("file", fileSelected, fileSelected.name);
            formData.append("product", data.id);
            if (data.branch) {
                formData.append("branch", data.branch);
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
            if (data.kubernetes_cluster) {
                formData.append("kubernetes_cluster", data.kubernetes_cluster);
            }
            formData.append("suppress_licenses", data.suppress_licenses);

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
        }
    };

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Upload" icon={<UploadIcon />} />
        </Toolbar>
    );
    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{
                    paddingTop: "0px",
                    paddingBottom: "2px",
                    color: getIconAndFontColor(),
                    textTransform: "none",
                    fontWeight: "normal",
                    fontSize: "1rem",
                }}
                startIcon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            >
                Upload observations from file
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Upload observations from file</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <input
                            id="sbom-input"
                            className={classes.input}
                            type="file"
                            onChange={handleFileChange}
                            accept=".csv, .json, .sarif"
                        />
                        <WithRecord
                            render={(product) => (
                                <ReferenceInput
                                    source="branch"
                                    reference="branches"
                                    sort={{ field: "name", order: "ASC" }}
                                    queryOptions={{ meta: { api_resource: "branch_names" } }}
                                    filter={{ product: product.id }}
                                    alwaysOn
                                >
                                    <AutocompleteInputWide optionText="name" label="Branch / Version" />
                                </ReferenceInput>
                            )}
                        />
                        <ReferenceInput
                            source="parser"
                            reference="parsers"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ source: "File" }}
                        >
                            <AutocompleteInputWide optionText="name" validate={validate_required} />
                        </ReferenceInput>
                        <TextInputWide source="service" validate={validate_255} />
                        <TextInputWide
                            source="docker_image_name_tag"
                            label="Docker image name:tag"
                            validate={validate_513}
                        />
                        <TextInputWide label="Endpoint URL" source="endpoint_url" validate={validate_2048} />
                        <TextInputWide source="kubernetes_cluster" validate={validate_255} />
                        <BooleanInput source="suppress_licenses" label="Suppress licenses" />
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
