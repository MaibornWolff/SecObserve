import AddIcon from "@mui/icons-material/Add";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, useCreate, useNotify, useRefresh } from "react-admin";
import { useFormContext } from "react-hook-form";

import { ROLE_CHOICES } from "../../access_control/types";
import CancelButton from "../../commons/custom_fields/CancelButton";
import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide } from "../../commons/layout/themes";

export type ProductAuthorizationGroupMemberAddProps = {
    id: any;
};

const ProductAuthorizationGroupMemberAdd = ({ id }: ProductAuthorizationGroupMemberAddProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => {
        resetState();
        setOpen(false);
    };
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        resetState();
        setOpen(false);
    };

    const [authorization_group, setAuthorizationGroup] = useState();
    const [role, setRole] = useState();
    const resetState = () => {
        setAuthorizationGroup(undefined);
        setRole(undefined);
    };

    const CustomToolbar = () => {
        const { reset } = useFormContext();

        const handleSaveContinue = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                authorization_group: authorization_group,
                role: role,
            };
            add_product_authorization_group_member(data, false);
        };

        const handleSaveClose = (e: any) => {
            e.preventDefault(); // necessary to prevent default SaveButton submit logic
            const data = {
                authorization_group: authorization_group,
                role: role,
            };
            add_product_authorization_group_member(data, true);
        };

        const add_product_authorization_group_member = (data: any, close_dialog: boolean) => {
            data.product = id;
            create(
                "product_authorization_group_members",
                { data: data },
                {
                    onSuccess: () => {
                        refresh();
                        notify("Authorization group member added", { type: "success" });
                        resetState();
                        reset();
                        if (close_dialog) {
                            setOpen(false);
                        }
                    },
                    onError: (error: any) => {
                        notify(error.message, { type: "warning" });
                    },
                }
            );
        };

        return (
            <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
                <CancelButton onClick={handleCancel} />
                <SaveButton
                    label="Save & Continue"
                    type="button"
                    onClick={handleSaveContinue}
                    sx={{ marginRight: 2 }}
                />
                <SaveButton type="button" onClick={handleSaveClose} />
            </Toolbar>
        );
    };

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
                    <SimpleForm onSubmit={create_product_authorization_group_member} toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="authorization_group"
                            reference="authorization_groups"
                            label="Authorization group"
                            filter={{ exclude_product: id }}
                            sort={{ field: "name", order: "ASC" }}
                        >
                            <AutocompleteInputWide
                                optionText="name"
                                validate={validate_required}
                                onChange={(e) => setAuthorizationGroup(e)}
                            />
                        </ReferenceInput>
                        <AutocompleteInputWide
                            source="role"
                            choices={ROLE_CHOICES}
                            validate={validate_required}
                            onChange={(e) => setRole(e)}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductAuthorizationGroupMemberAdd;
