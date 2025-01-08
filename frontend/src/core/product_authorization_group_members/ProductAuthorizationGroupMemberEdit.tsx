import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, useNotify, useRefresh, useUpdate } from "react-admin";

import { ROLE_CHOICES } from "../../access_control/types";
import CancelButton from "../../commons/custom_fields/CancelButton";
import EditButton from "../../commons/custom_fields/EditButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";

const ProductAuthorizationGroupMemberEdit = () => {
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
    const product_authorization_group_member_update = async (data: any) => {
        const patch = {
            role: data.role,
        };

        update(
            "product_authorization_group_members",

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
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    return (
        <Fragment>
            <EditButton title="Edit" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit authorization group member</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={product_authorization_group_member_update} toolbar={<CustomToolbar />}>
                        <TextInputWide source="authorization_group_data.name" label="Authorization group" disabled />
                        <AutocompleteInputWide source="role" choices={ROLE_CHOICES} validate={validate_required} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductAuthorizationGroupMemberEdit;
