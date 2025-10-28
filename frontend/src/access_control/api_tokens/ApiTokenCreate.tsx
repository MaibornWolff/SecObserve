import AddIcon from "@mui/icons-material/Add";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack, TextField } from "@mui/material";
import { useState } from "react";
import { SimpleForm, useNotify, useRefresh } from "react-admin";

import AddButton from "../../commons/custom_fields/AddButton";
import CopyToClipboardButton from "../../commons/custom_fields/CopyToClipboardButton";
import { ToolbarCancelSave } from "../../commons/custom_fields/ToolbarCancelSave";
import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, PasswordInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { ROLE_CHOICES } from "../types";

type ApiTokenCreateProps = {
    type: "user" | "product";
    product?: any;
    user?: any;
};

const ApiTokenCreate = ({ type, product, user }: ApiTokenCreateProps) => {
    const refresh = useRefresh();
    const notify = useNotify();

    const [roleOpen, setRoleOpen] = useState(false);
    const handleRoleOpen = () => setRoleOpen(true);
    const handleRoleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setRoleOpen(false);
    };

    const handleRoleCancel = () => setRoleOpen(false);

    const [apiToken, setApiToken] = useState("undefined");

    const [showApiTokenOpen, setShowApiTokenOpen] = useState(false);
    const handleApiTokenOpen = () => setShowApiTokenOpen(true);
    const handleApiTokenClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        handleApiTokenOk();
    };
    const handleApiTokenOk = () => {
        setApiToken("undefined");
        setShowApiTokenOpen(false);
        refresh();
    };

    const handleApiTokenCreate = async (data: any) => {
        let url = "";
        let create_data = undefined;
        if (type === "product") {
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/product_api_tokens/";
            create_data = {
                id: product.id,
                role: data.role,
            };
        } else if (type === "user") {
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/authentication/create_user_api_token/";
            create_data = {
                username: user.username,
                password: data.password,
            };
        } else {
            notify("Type is not product or user", { type: "error" });
            setRoleOpen(false);
            return;
        }

        httpClient(url, {
            method: "POST",
            body: JSON.stringify(create_data),
        })
            .then((result) => {
                setApiToken(result.json.token);
                handleApiTokenOpen();
                notify("Product API token created", {
                    type: "success",
                });
                setRoleOpen(false);
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    return (
        <>
            <AddButton title="Create API token" onClick={handleRoleOpen} />
            <Dialog open={roleOpen} onClose={handleRoleClose}>
                <DialogTitle>Create {type} API token</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={handleApiTokenCreate}
                        toolbar={
                            <ToolbarCancelSave
                                onClick={handleRoleCancel}
                                saveButtonLabel="Create"
                                saveButtonIcon={<AddIcon />}
                            />
                        }
                    >
                        {type === "product" && (
                            <AutocompleteInputWide source="role" choices={ROLE_CHOICES} validate={validate_required} />
                        )}
                        {type === "user" && (
                            <PasswordInputWide source="password" label="Password" validate={validate_required_255} />
                        )}
                    </SimpleForm>
                </DialogContent>
            </Dialog>
            <Dialog open={showApiTokenOpen} onClose={handleApiTokenClose}>
                <DialogTitle>Create {type} API token</DialogTitle>
                <DialogContent>
                    <Stack
                        direction="row"
                        spacing={2}
                        justifyContent="center"
                        alignItems="center"
                        sx={{ marginBottom: 4 }}
                    >
                        <TextField disabled defaultValue={apiToken} sx={{ width: "50ch" }} />
                        <CopyToClipboardButton text={apiToken} />
                    </Stack>
                    Make sure to copy the token now. You won&apos;t be able to see it again!
                </DialogContent>
                <DialogActions>
                    <Button variant="contained" color="inherit" onClick={handleApiTokenOk}>
                        OK
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

export default ApiTokenCreate;
