import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";
import { useFormContext } from "react-hook-form";

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
    const [license, setLicense] = useState();

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
                marginLeft: 2,
            }}
            variant="contained"
            onClick={handleCancel}
            color="inherit"
            startIcon={<CancelIcon />}
        >
            Cancel
        </Button>
    );

    const CustomToolbar = () => {
        const { reset } = useFormContext();

        const handleSaveContinue = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                license: license,
            };
            add_license(data, false);
        };

        const handleSaveClose = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                license: license,
            };
            add_license(data, true);
        };

        const add_license = (data: any, close_dialog: boolean) => {
            const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_groups/" + id + "/add_license/";
            const body = JSON.stringify({ license: data.license });
            httpClient(url, {
                method: "POST",
                body: body,
            })
                .then(() => {
                    refresh();
                    notify("License added", { type: "success" });
                    reset();
                    if (close_dialog) {
                        setOpen(false);
                    }
                })
                .catch((error) => {
                    notify(error.message, { type: "warning" });
                });
        };

        return (
            <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
                <CancelButton />
                <SaveButton
                    label="Save & Continue"
                    type="button"
                    onClick={handleSaveContinue}
                    sx={{ marginRight: 2 }}
                />
                <SaveButton type="button" onClick={handleSaveClose} />
            </Toolbar>
        );
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
                    <SimpleForm toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="license"
                            reference="licenses"
                            label="License"
                            sort={{ field: "spdx_id", order: "ASC" }}
                        >
                            <AutocompleteInputWide
                                optionText="spdx_id"
                                validate={validate_required}
                                onChange={(e) => setLicense(e)}
                            />
                        </ReferenceInput>
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicenseGroupLicenseAdd;
