import CancelIcon from "@mui/icons-material/Cancel";
import LibraryAddIcon from "@mui/icons-material/LibraryAdd";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { CreateBase, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";
import { useNavigate } from "react-router";

import { validate_required } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

type LicensePolicyCopyProps = {
    license_policy: any;
};

const LicensePolicyCopy = ({ license_policy }: LicensePolicyCopyProps) => {
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
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
            <SaveButton label="Copy" icon={<LibraryAddIcon />} />
        </Toolbar>
    );

    const copyLicensePolicy = (data: any) => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policies/" + license_policy.id + "/copy/";
        const body = JSON.stringify({ name: data.new_name });
        httpClient(url, {
            method: "POST",
            body: body,
        })
            .then((response) => {
                refresh();
                notify("License policy copied", { type: "success" });
                navigate("/license_policies/" + response.json.id + "/show");
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });
    };

    return (
        <Fragment>
            <Button
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                onClick={handleOpen}
                startIcon={<LibraryAddIcon />}
            >
                Copy
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Copy license policy</DialogTitle>
                <DialogContent>
                    <CreateBase resource="license_policy_members">
                        <SimpleForm onSubmit={copyLicensePolicy} toolbar={<CustomToolbar />}>
                            <TextInputWide source="new_name" label="Name" validate={validate_required} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyCopy;
