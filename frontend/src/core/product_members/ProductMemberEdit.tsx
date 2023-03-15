import * as React from "react";
import {
    SimpleForm,
    required,
    useRefresh,
    useNotify,
    SaveButton,
    Toolbar,
    useUpdate,
    ReferenceInput,
} from "react-admin";
import { Dialog, DialogTitle, DialogContent, Button } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import CancelIcon from "@mui/icons-material/Cancel";

import { ROLE_CHOICES } from "../../access_control/types";
import { AutocompleteInputWide } from "../../commons/layout/themes";

const ProductMemberEdit = () => {
    const [open, setOpen] = React.useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();

    const product_member_update = async (data: any) => {
        const patch = {
            role: data.role,
        };

        update(
            "product_members",

            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("Product member updated", {
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

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
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
            onClick={handleClose}
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
                <DialogTitle>Edit product member</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={product_member_update}
                        toolbar={<CustomToolbar />}
                    >
                        <ReferenceInput
                            source="user"
                            reference="users"
                            sort={{ field: "full_name", order: "ASC" }}
                        >
                            <AutocompleteInputWide
                                optionText="full_name"
                                disabled
                            />
                        </ReferenceInput>
                        <AutocompleteInputWide
                            source="role"
                            choices={ROLE_CHOICES}
                            validate={requiredValidate}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ProductMemberEdit;
