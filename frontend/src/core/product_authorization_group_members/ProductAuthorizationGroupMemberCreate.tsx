import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { ROLE_CHOICES } from "../../access_control/types";
import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide } from "../../commons/layout/themes";

export type ProductAuthorizationGroupMemberCreateProps = {
    id: any;
};

const ProductAuthorizationGroupMemberCreate = ({ id }: ProductAuthorizationGroupMemberCreateProps) => {
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

    const create_product_authorization_group_member = (data: any) => {
        data.product = id;
        create(
            "product_authorization_group_members",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Authorization group member added", { type: "success" });
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
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem", marginBottom: 1 }}
                startIcon={<AddIcon />}
            >
                Add authorization group member
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add authorization group member</DialogTitle>
                <DialogContent>
                    <CreateBase resource="product_authorization_group_members">
                        <SimpleForm onSubmit={create_product_authorization_group_member} toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="authorization_group"
                                reference="authorization_groups"
                                label="Authorization group"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="name" validate={validate_required} />
                            </ReferenceInput>
                            <AutocompleteInputWide source="role" choices={ROLE_CHOICES} validate={validate_required} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductAuthorizationGroupMemberCreate;
