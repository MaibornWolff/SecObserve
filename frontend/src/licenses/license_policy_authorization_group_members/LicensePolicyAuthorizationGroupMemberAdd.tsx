import AddIcon from "@mui/icons-material/Add";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { BooleanInput, ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";
import { useFormContext } from "react-hook-form";

import CancelButton from "../../commons/custom_fields/CancelButton";
import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

export type LicensePolicyAuthorizationGroupMemberAddProps = {
    id: any;
};

const LicensePolicyAuthorizationGroupMemberAdd = ({ id }: LicensePolicyAuthorizationGroupMemberAddProps) => {
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

    const [authorization_group, setAuthorizationGroup] = useState();
    const [is_manager, setIsManager] = useState(false);
    const resetState = () => {
        setAuthorizationGroup(undefined);
        setIsManager(false);
    };

    const CustomToolbar = () => {
        const { reset } = useFormContext();

        const handleSaveContinue = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                authorization_group: authorization_group,
                is_manager: is_manager,
            };
            add_authorization_group(data, false);
        };

        const handleSaveClose = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                authorization_group: authorization_group,
                is_manager: is_manager,
            };
            add_authorization_group(data, true);
        };

        const add_authorization_group = (data: any, close_dialog: boolean) => {
            const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policy_authorization_group_members/";
            const body = JSON.stringify({ license_policy: id, ...data });
            httpClient(url, {
                method: "POST",
                body: body,
            })
                .then(() => {
                    refresh();
                    notify("Authorization group added", { type: "success" });
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
                <CancelButton onClick={handleCancel} />
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
                Add authorization group
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add authorization group</DialogTitle>
                <DialogContent>
                    <SimpleForm toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="authorization_group"
                            reference="authorization_groups"
                            label="Authorization group"
                            filter={{ exclude_license_policy: id }}
                            sort={{ field: "name", order: "ASC" }}
                        >
                            <AutocompleteInputWide
                                optionText="name"
                                validate={validate_required}
                                onChange={(e) => setAuthorizationGroup(e)}
                            />
                        </ReferenceInput>
                        <BooleanInput
                            source="is_manager"
                            label="Manager"
                            onChange={(e) => setIsManager(e.target.checked)}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyAuthorizationGroupMemberAdd;
