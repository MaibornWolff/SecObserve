import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { BooleanInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh, useUpdate } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import { TextInputWide } from "../../commons/layout/themes";
import EditButton from "../../commons/custom_fields/EditButton";

const LicensePolicyAuthorizationGroupMemberEdit = () => {
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

    const member_update = async (data: any) => {
        const patch = {
            is_manager: data.is_manager,
        };

        update(
            "license_policy_authorization_group_members",

            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("Authorization group member updated", {
                        type: "success",
                    });
                },
                onError: (error: any) => {
                    notify(error.message, {
                        type: "warning",
                    });
                },
            }
        );
        setOpen(false);
    };

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    return (
        <Fragment>
            <EditButton title="Edit" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit authorization group</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={member_update} toolbar={<CustomToolbar />}>
                        <TextInputWide source="authorization_group_data.name" label="Authorization group" disabled />
                        <BooleanInput source="is_manager" label="Manager" />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyAuthorizationGroupMemberEdit;
