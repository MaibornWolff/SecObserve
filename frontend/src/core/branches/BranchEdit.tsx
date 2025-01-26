import { Dialog, DialogContent, DialogTitle, Stack } from "@mui/material";
import { Fragment, useState } from "react";
import { BooleanInput, SaveButton, SimpleForm, useNotify, useRefresh, useUpdate } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import EditButton from "../../commons/custom_fields/EditButton";
import OSVEcosystemInput from "../../commons/custom_fields/OSVEcosystemInput";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_255, validate_required_255 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";

export type BranchEditProps = {
    product: any;
};

const BranchEdit = ({ product }: BranchEditProps) => {
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
    const branch_update = async (data: any) => {
        if (!data.purl) {
            data.purl = "";
        }
        if (!data.cpe23) {
            data.cpe23 = "";
        }
        if (!data.osv_linux_ecosystem) {
            data.osv_linux_ecosystem = "";
        }
        if (!data.osv_linux_release) {
            data.osv_linux_release = "";
        }

        const patch = {
            name: data.name,
            housekeeping_protect: data.housekeeping_protect,
            purl: data.purl,
            cpe23: data.cpe23,
            osv_linux_ecosystem: data.osv_linux_ecosystem,
            osv_linux_release: data.osv_linux_release,
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
                    notify("Branch / version updated", {
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

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );
    return (
        <Fragment>
            <EditButton title="Edit" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Edit branch / version</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={branch_update} toolbar={<CustomToolbar />}>
                        <TextInputWide source="name" validate={validate_required_255} />
                        <TextInputWide source="purl" label="PURL" validate={validate_255} />
                        <TextInputWide source="cpe23" label="CPE 2.3" validate={validate_255} />
                        <BooleanInput source="housekeeping_protect" label="Protect from housekeeping" />
                        {product && product.osv_enabled && (
                            <Stack direction="row" spacing={2} alignItems="center">
                                <OSVEcosystemInput />
                            </Stack>
                        )}
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default BranchEdit;
