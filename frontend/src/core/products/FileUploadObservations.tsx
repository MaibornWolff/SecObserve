import CancelIcon from "@mui/icons-material/Cancel";
import UploadIcon from "@mui/icons-material/Upload";
import { Button, Dialog, DialogContent, DialogTitle, LinearProgress } from "@mui/material";
import { ChangeEvent, Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, required, useNotify, useRefresh } from "react-admin";
import { makeStyles } from "tss-react/mui";

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

            httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/import/file_upload_observations_by_id/", {
                method: "POST",
                body: formData,
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
                    notify(message, {
                        type: "success",
                    });
                })
                .catch((error) => {
                    notify(error.message, {
                        type: "warning",
                    });
                });
            setLoading(false);
            setOpen(false);
        }
    };

    const handleClose = () => {
        setOpen(false);
        setLoading(false);
    };

    const handleOpen = () => {
        setOpen(true);
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
            <SaveButton label="Upload" icon={<UploadIcon />} />
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
                Upload Observations From File
            </Button>
            <Dialog open={open} onClose={handleClose}>
                {loading ? <LinearProgress color="secondary" /> : null}
                <DialogTitle>Upload Observations From File</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <input
                            id="sbom-input"
                            className={classes.input}
                            type="file"
                            onChange={handleFileChange}
                            accept=".json, .sarif"
                        />
                        <ReferenceInput
                            source="parser"
                            reference="parsers"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ source: "File" }}
                        >
                            <AutocompleteInputWide optionText="name" validate={requiredValidate} />
                        </ReferenceInput>
                        <TextInputWide source="service" />
                        <TextInputWide source="docker_image_name_tag" label="Docker image name:tag" />
                        <TextInputWide source="endpoint_url" />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

const requiredValidate = [required()];

export default FileUploadObservations;
