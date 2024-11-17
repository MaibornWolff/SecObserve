import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { CreateBase, ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";
import { useFormContext } from "react-hook-form";

import { validate_255, validate_required } from "../../commons/custom_validators";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { EVALUATION_RESULT_CHOICES } from "../types";

export type LicensePolicyItemAddProps = {
    id: any;
};

const LicensePolicyItemAdd = ({ id }: LicensePolicyItemAddProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => {
        resetState();
        setOpen(false);
    };
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        resetState();
        setOpen(false);
    };

    const [license_group, setLicenseGroup] = useState();
    const [license, setLicense] = useState();
    const [unknown_license, setUnknownLicense] = useState();
    const [evaluation_result, setEvaluationResult] = useState();

    const resetState = () => {
        setLicenseGroup(undefined);
        setLicense(undefined);
        setUnknownLicense(undefined);
        setEvaluationResult(undefined);
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

    const CustomToolbar = () => {
        const { reset } = useFormContext();

        const handleSaveContinue = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            add_item(setData(), false);
        };

        const handleSaveClose = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            add_item(setData(), true);
        };

        const setData = () => {
            const data = {
                license_group: license_group,
                license: license,
                unknown_license: unknown_license,
                evaluation_result: evaluation_result,
            };
            return data;
        };

        const add_item = (data: any, close_dialog: boolean) => {
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
                    resetState();
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
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem", marginBottom: 1 }}
                startIcon={<AddIcon />}
            >
                Add license policy item
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add license policy item</DialogTitle>
                <DialogContent>
                    <CreateBase resource="license_policy_items">
                        <SimpleForm toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="license_group"
                                reference="license_groups"
                                label="License group"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="name" onChange={(e) => setLicenseGroup(e)} />
                            </ReferenceInput>
                            <ReferenceInput
                                source="license"
                                reference="licenses"
                                label="License"
                                sort={{ field: "spdx_id", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="spdx_id" onChange={(e) => setLicense(e)} />
                            </ReferenceInput>
                            <TextInputWide
                                source="unknown_license"
                                label="Unknown license"
                                validate={validate_255}
                                onChange={(e) => setUnknownLicense(e.target.value)}
                            />
                            <AutocompleteInputMedium
                                source="evaluation_result"
                                label="Evaluation result"
                                choices={EVALUATION_RESULT_CHOICES}
                                validate={validate_required}
                                onChange={(e) => setEvaluationResult(e)}
                            />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyItemAdd;
