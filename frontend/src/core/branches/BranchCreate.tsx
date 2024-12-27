import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { BooleanInput, CreateBase, SaveButton, SimpleForm, useCreate, useNotify, useRefresh } from "react-admin";

import AddButton from "../../commons/custom_fields/AddButton";
import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_255, validate_required_255 } from "../../commons/custom_validators";
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

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
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
                    notify("Branch / version added", { type: "success" });
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
            <AddButton title="Add branch / version" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add branch / version</DialogTitle>
                <DialogContent>
                    <CreateBase resource="branches">
                        <SimpleForm onSubmit={create_branch} toolbar={<CustomToolbar />}>
                            <TextInputWide source="name" validate={validate_required_255} />
                            <TextInputWide source="purl" label="PURL" validate={validate_255} />
                            <TextInputWide source="cpe23" label="CPE 2.3" validate={validate_255} />
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
