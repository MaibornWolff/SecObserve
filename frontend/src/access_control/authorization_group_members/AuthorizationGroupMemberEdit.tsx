import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { BooleanInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh, useUpdate } from "react-admin";

import { TextInputWide } from "../../commons/layout/themes";

const ProductMemberEdit = () => {
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
            "authorization_group_members",

            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("User member updated", {
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
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit user</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={member_update} toolbar={<CustomToolbar />}>
                        <TextInputWide source="user_data.full_name" label="User" disabled />
                        <BooleanInput source="is_manager" label="Manager" />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductMemberEdit;
