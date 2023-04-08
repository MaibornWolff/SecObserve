import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import {
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { ROLE_CHOICES } from "../../access_control/types";
import { AutocompleteInputWide } from "../../commons/layout/themes";

export type ProductMemberCreateProps = {
    id: any;
};

const ProductMemberCreate = ({ id }: ProductMemberCreateProps) => {
    const [open, setOpen] = React.useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const [create] = useCreate();

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
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

    const create_product_member = (data: any) => {
        data.product = id;
        create(
            "product_members",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Product member added", { type: "success" });
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
        setOpen(false);
    };

    return (
        <React.Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Add product member
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add product member</DialogTitle>
                <DialogContent>
                    <CreateBase resource="product_members">
                        <SimpleForm onSubmit={create_product_member} toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="user"
                                reference="users"
                                label="User Category"
                                sort={{ field: "full_name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="full_name" validate={requiredValidate} />
                            </ReferenceInput>
                            <AutocompleteInputWide source="role" choices={ROLE_CHOICES} validate={requiredValidate} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ProductMemberCreate;
