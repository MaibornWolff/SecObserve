import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { ChangeEvent, Fragment, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";
import { makeStyles } from "tss-react/mui";

import CancelButton from "../../commons/custom_fields/CancelButton";
import SmallButton from "../../commons/custom_fields/SmallButton";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const VEXDocumentImport = () => {
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

    const vexImport = async () => {
        if (fileSelected) {
            setLoading(true);

            const formData = new FormData();
            formData.append("file", fileSelected, fileSelected.name);

            httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/vex/vex_import/", {
                method: "POST",
                body: formData,
            })
                .then(() => {
                    refresh();
                    setLoading(false);
                    setOpen(false);
                    notify("VEX document imported", {
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
        }
    };

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Import" icon={<UploadIcon />} alwaysEnable />
        </Toolbar>
    );
    return (
        <Fragment>
            <SmallButton title="Import VEX document" onClick={handleOpen} icon={<UploadIcon />} />
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Import VEX document</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={vexImport} toolbar={<CustomToolbar />}>
                        <input
                            id="vex-input"
                            className={classes.input}
                            type="file"
                            onChange={handleFileChange}
                            accept=".json"
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

export default VEXDocumentImport;
