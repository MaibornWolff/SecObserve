import DeleteIcon from "@mui/icons-material/Delete";
import { Dialog, DialogContent, DialogTitle, Typography } from "@mui/material";
import { useState } from "react";
import { SaveButton, SimpleForm, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import RemoveButton from "../../commons/custom_fields/RemoveButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_required_255 } from "../../commons/custom_validators";
import { PasswordInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

type ApiTokenRevokeProps = {
    type: "user" | "product";
    product?: any;
    user?: any;
};

const ApiTokenRevoke = ({ type, product, user }: ApiTokenRevokeProps) => {
    const refresh = useRefresh();
    const notify = useNotify();

    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleApiTokenRevoke = async (data: any) => {
        let method = "";
        let url = "";
        let revoke_data = undefined;

        if (type === "product") {
            method = "DELETE";
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/product_api_tokens/" + product.id + "/";
        } else if (type === "user") {
            method = "POST";
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/authentication/revoke_user_api_token/";
            revoke_data = {
                username: user.username,
                password: data.password,
            };
        } else {
            notify("Type is not product or user", { type: "error" });
            setOpen(false);
            return;
        }

        httpClient(url, {
            method: method,
            body: type === "user" ? JSON.stringify(revoke_data) : null,
        })
            .then(() => {
                notify("API token revoked", {
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

    return (
        <>
            <RemoveButton title="Revoke" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Revoke {type} API token</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={handleApiTokenRevoke}
                        toolbar={
                            <Toolbar>
                                <CancelButton onClick={handleClose} />
                                <SaveButton
                                    label="Revoke"
                                    color="error"
                                    icon={<DeleteIcon />}
                                    alwaysEnable={type === "product"}
                                />
                            </Toolbar>
                        }
                    >
                        <Typography sx={{ marginBottom: 2 }}>
                            Are you sure you want to revoke the {type} API token?
                        </Typography>
                        {type === "user" && (
                            <PasswordInputWide source="password" label="Password" validate={validate_required_255} />
                        )}
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </>
    );
};

export default ApiTokenRevoke;
