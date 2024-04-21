import DeleteIcon from "@mui/icons-material/Delete";
import { Button, Typography } from "@mui/material";
import { useState } from "react";
import { Confirm, useNotify } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

const JWTSecretReset = () => {
    const notify = useNotify();

    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleJWTSecretReset = async () => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/jwt_secret/reset/";
        httpClient(url, {
            method: "POST",
        })
            .then(() => {
                notify("JWT secret reset", {
                    type: "success",
                });
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });

        setOpen(false);
    };

    const body = `Are you sure you want to reset the JWT secret?
    This will invalidate all existing JWT tokens.`;

    return (
        <>
            <Button sx={{ color: "#d32f2f" }} onClick={handleOpen} startIcon={<DeleteIcon />}>
                Reset JWT secret
            </Button>
            <Confirm
                isOpen={open}
                title="Reset JWT secret"
                content={<Typography sx={{ whiteSpace: "pre-line" }}>{body}</Typography>}
                onConfirm={handleJWTSecretReset}
                onClose={handleClose}
            />
        </>
    );
};

export default JWTSecretReset;
