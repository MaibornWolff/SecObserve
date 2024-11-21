import UploadIcon from "@mui/icons-material/Upload";
import { Backdrop, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Button, Confirm, useNotify, useRefresh } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ImportScanCodeLicenseDB = () => {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const importScanCodeLicenseDB = async () => {
        setLoading(true);
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_groups/import_scancode_licensedb/";
        httpClient(url, {
            method: "POST",
        })
            .then(() => {
                refresh();
                setLoading(false);
                notify("ScanCode LicenseDB imported", { type: "success" });
            })
            .catch((error) => {
                setLoading(false);
                notify(error.message, { type: "warning" });
            });

        setOpen(false);
    };

    return (
        <>
            <Button
                label="Import ScanCode LicenseDB"
                onClick={handleClick}
                startIcon={<UploadIcon />}
                variant="contained"
                sx={{ width: "fit-content", fontSize: "0.8125rem", paddingBottom: 1, paddingTop: 1 }}
            />
            <Confirm
                isOpen={open}
                title="Import ScanCode LicenseDB"
                content={"Are you sure you want to import license groups from the ScanCode LicenseDB?"}
                onConfirm={importScanCodeLicenseDB}
                onClose={handleDialogClose}
            />
            {loading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </>
    );
};

export default ImportScanCodeLicenseDB;
