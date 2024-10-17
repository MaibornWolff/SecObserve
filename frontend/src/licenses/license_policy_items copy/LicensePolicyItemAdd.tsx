import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { CreateBase, ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";

import { validate_255, validate_required } from "../../commons/custom_validators";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { LICENSE_POLICY_EVALUATION_RESULT_CHOICES } from "../types";

export type LicensePolicyItemAddProps = {
    id: any;
};

const LicensePolicyItemAdd = ({ id }: LicensePolicyItemAddProps) => {
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

    const add_user = (data: any) => {
        if (!data.unknown_license) {
            data.unknown_license = "";
        }
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policy_items/";
        const body = JSON.stringify({ license_policy: id, ...data });
        httpClient(url, {
            method: "POST",
            body: body,
        })
            .then(() => {
                refresh();
                notify("Item added", { type: "success" });
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
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem", marginBottom: 1 }}
                startIcon={<AddIcon />}
            >
                Add license policy item
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add license policy item</DialogTitle>
                <DialogContent>
                    <CreateBase resource="license_policy_items">
                        <SimpleForm onSubmit={add_user} toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="license_group"
                                reference="license_groups"
                                label="License group"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="name" />
                            </ReferenceInput>
                            <ReferenceInput
                                source="license"
                                reference="licenses"
                                label="License"
                                sort={{ field: "spdx_id", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="spdx_id" />
                            </ReferenceInput>
                            <TextInputWide source="unknown_license" label="Unknown license" validate={validate_255} />
                            <AutocompleteInputMedium
                                source="evaluation_result"
                                label="Evaluation result"
                                choices={LICENSE_POLICY_EVALUATION_RESULT_CHOICES}
                                validate={validate_required}
                            />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyItemAdd;
