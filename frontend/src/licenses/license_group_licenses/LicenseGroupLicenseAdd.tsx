import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";

import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

export type LicenseGroupLicenseAddProps = {
    id: any;
};

const LicenseGroupLicenseAdd = ({ id }: LicenseGroupLicenseAddProps) => {
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
            <SaveButton />
        </Toolbar>
    );

    const add_license = (data: any) => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_groups/" + id + "/add_license/";
        const body = JSON.stringify({ license: data.license });
        httpClient(url, {
            method: "POST",
            body: body,
        })
            .then(() => {
                refresh();
                notify("License added", { type: "success" });
                setOpen(false);
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });
    };

    return (
        <Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem", marginBottom: 1, marginTop: 1 }}
                startIcon={<AddIcon />}
            >
                Add license
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add license</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={add_license} toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="license"
                            reference="licenses"
                            label="License"
                            sort={{ field: "spdx_id", order: "ASC" }}
                        >
                            <AutocompleteInputWide optionText="spdx_id" validate={validate_required} />
                        </ReferenceInput>
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicenseGroupLicenseAdd;
