import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    BooleanInput,
    CreateBase,
    SaveButton,
    SimpleForm,
    Toolbar,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

export type BranchCreateProps = {
    id: any;
};

const BranchCreate = ({ id }: BranchCreateProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
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

    const create_branch = (data: any) => {
        data.product = id;
        create(
            "branches",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Branch added", { type: "success" });
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
        setOpen(false);
    };

    return (
        <Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Add branch
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add branch</DialogTitle>
                <DialogContent>
                    <CreateBase resource="branches">
                        <SimpleForm onSubmit={create_branch} toolbar={<CustomToolbar />}>
                            <TextInputWide source="name" validate={validate_required_255} />
                            <BooleanInput
                                source="housekeeping_protect"
                                label="Protect from housekeeping"
                                defaultValue={false}
                            />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default BranchCreate;
