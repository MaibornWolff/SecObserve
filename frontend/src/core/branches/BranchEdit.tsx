import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import { BooleanInput, SaveButton, SimpleForm, Toolbar, required, useNotify, useRefresh, useUpdate } from "react-admin";

import { TextInputWide } from "../../commons/layout/themes";

const BranchEdit = () => {
    const [open, setOpen] = React.useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };
    const branch_update = async (data: any) => {
        const patch = {
            name: data.name,
            housekeeping_protect: data.housekeeping_protect,
        };

        update(
            "branches",
            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("Branch updated", {
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
                color: "#000000dd",
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
        <React.Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<EditIcon />}
            >
                Edit
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit branch</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={branch_update} toolbar={<CustomToolbar />}>
                        <TextInputWide source="name" validate={requiredValidate} />
                        <BooleanInput source="housekeeping_protect" label="Protect from housekeeping" />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default BranchEdit;
