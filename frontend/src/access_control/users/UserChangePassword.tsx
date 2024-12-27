import PasswordIcon from "@mui/icons-material/Password";
import { Dialog, DialogContent, DialogTitle, Typography } from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, WithRecord, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import SmallButton from "../../commons/custom_fields/SmallButton";
import { validate_required_255 } from "../../commons/custom_validators";
import { PasswordInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const UserChangePassword = () => {
    const refresh = useRefresh();
    const [open, setOpen] = useState(false);
    const notify = useNotify();
    const [password_rules, setPasswordRules] = useState("");

    useEffect(() => {
        get_password_rules();
    }, []);

    function get_password_rules() {
        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/password_rules/", {
            method: "GET",
        }).then((result) => {
            setPasswordRules(result.json.password_rules);
        });
    }

    const changePassword = async (data: any) => {
        const patch = {
            current_password: data.current_password,
            new_password_1: data.new_password_1,
            new_password_2: data.new_password_2,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/" + data.id + "/change_password/", {
            method: "PATCH",
            body: JSON.stringify(patch),
        })
            .then(() => {
                notify("Password changed", {
                    type: "success",
                });
                refresh();
                setOpen(false);
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const handleCancel = () => setOpen(false);

    const handleOpen = () => setOpen(true);

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Change" />
        </Toolbar>
    );
    return (
        <Fragment>
            <SmallButton title="Change password" onClick={handleOpen} icon={<PasswordIcon />} />
            <WithRecord
                render={(user) => (
                    <Dialog open={open} onClose={handleClose}>
                        <DialogTitle>Change password for {user.full_name}</DialogTitle>
                        <DialogContent>
                            <SimpleForm onSubmit={changePassword} toolbar={<CustomToolbar />}>
                                <PasswordInputWide
                                    source="current_password"
                                    label="Your current password"
                                    validate={validate_required_255}
                                />
                                <PasswordInputWide source="new_password_1" validate={validate_required_255} />
                                <PasswordInputWide source="new_password_2" validate={validate_required_255} />
                                <Typography sx={{ fontWeight: "bold" }}>Password rules:</Typography>
                                <Typography sx={{ whiteSpace: "pre-line" }}>{password_rules}</Typography>
                            </SimpleForm>
                        </DialogContent>
                    </Dialog>
                )}
            />
        </Fragment>
    );
};

export default UserChangePassword;
