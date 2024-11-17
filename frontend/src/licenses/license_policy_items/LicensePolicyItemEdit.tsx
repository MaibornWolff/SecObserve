import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh, useUpdate } from "react-admin";

import { validate_255, validate_required } from "../../commons/custom_validators";
import { AutocompleteInputExtraWide, AutocompleteInputMedium, TextInputExtraWide } from "../../commons/layout/themes";
import { EVALUATION_RESULT_CHOICES } from "../types";

const LicensePolicyItemEdit = () => {
    const [open, setOpen] = useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const item_update = async (data: any) => {
        if (!data.unknown_license) {
            data.unknown_license = "";
        }
        const patch = {
            license_group: data.license_group,
            license: data.license,
            unknown_license: data.unknown_license,
            evaluation_result: data.evaluation_result,
        };

        update(
            "license_policy_items",

            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("License policy item updated", {
                        type: "success",
                    });
                    setOpen(false);
                },
                onError: (error: any) => {
                    notify(error.message, {
                        type: "warning",
                    });
                },
            }
        );
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
    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<EditIcon />}
            >
                Edit
            </Button>
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Edit license policy item</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={item_update} toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="license_group"
                            reference="license_groups"
                            label="License group"
                            sort={{ field: "name", order: "ASC" }}
                        >
                            <AutocompleteInputExtraWide optionText="name" />
                        </ReferenceInput>
                        <ReferenceInput
                            source="license"
                            reference="licenses"
                            label="License"
                            sort={{ field: "spdx_id", order: "ASC" }}
                        >
                            <AutocompleteInputExtraWide optionText="spdx_id_name" />
                        </ReferenceInput>
                        <TextInputExtraWide source="unknown_license" label="Unknown license" validate={validate_255} />
                        <AutocompleteInputMedium
                            source="evaluation_result"
                            label="Evaluation result"
                            choices={EVALUATION_RESULT_CHOICES}
                            validate={validate_required}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyItemEdit;
