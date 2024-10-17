import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useNotify,
    useRefresh,
} from "react-admin";

import { validate_required } from "../../commons/custom_validators";
import { AutocompleteInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

export type LicensePolicyMemberAddProps = {
    id: any;
};

const LicensePolicyMemberAdd = ({ id }: LicensePolicyMemberAddProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
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

    const add_user = (data: any) => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policy_members/";
        const body = JSON.stringify({ license_policy: id, ...data });
        httpClient(url, {
            method: "POST",
            body: body,
        })
            .then(() => {
                refresh();
                notify("User added", { type: "success" });
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });

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
                Add user
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add user</DialogTitle>
                <DialogContent>
                    <CreateBase resource="license_policy_members">
                        <SimpleForm onSubmit={add_user} toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="user"
                                reference="users"
                                label="User"
                                sort={{ field: "full_name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="full_name" validate={validate_required} />
                            </ReferenceInput>
                            <BooleanInput source="is_manager" label="Manager" />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyMemberAdd;
