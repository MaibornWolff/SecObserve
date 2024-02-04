import LockIcon from "@mui/icons-material/Lock";
import PersonIcon from "@mui/icons-material/Person";
import { Avatar, Button, Card, CardActions, CircularProgress, Stack } from "@mui/material";
import Box from "@mui/material/Box";
import PropTypes from "prop-types";
import { Fragment } from "react";
import { useState } from "react";
import { Form, TextInput, required, useLogin, useNotify, useTheme } from "react-admin";
import { useAuth } from "react-oidc-context";
import { Navigate, useLocation } from "react-router-dom";

import { getTheme } from "../commons/settings/functions";
import { OIDCSignInButton } from "./OIDCSignInButton";
import { jwt_signed_in } from "./authProvider";

const Login = () => {
    const [loading, setLoading] = useState(false);
    const [, setTheme] = useTheme();
    const auth = useAuth();

    const notify = useNotify();
    const login = useLogin();
    const location = useLocation();
    const isAuthenticated = jwt_signed_in() || auth.isAuthenticated;

    const handleSubmit = (auth: FormValues) => {
        setLoading(true);
        login(auth, location.state ? (location.state as any).nextPathname : "/")
            .then(() => {
                setTheme(getTheme());
            })
            .catch((error: Error) => {
                setLoading(false);
                notify(
                    typeof error === "string"
                        ? error
                        : typeof error === "undefined" || !error.message
                          ? "ra.auth.sign_in_error"
                          : error.message,
                    {
                        type: "warning",
                        messageArgs: {
                            _: typeof error === "string" ? error : error && error.message ? error.message : undefined,
                        },
                    }
                );
            });
    };

    return (
        <Fragment>
            {isAuthenticated && <Navigate to="/" replace={true} />}
            {!isAuthenticated && !auth.isLoading && (
                <Form onSubmit={handleSubmit} noValidate>
                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: "column",
                            minHeight: "100vh",
                            alignItems: "center",
                            justifyContent: "center",
                            background: "url(background_login.png)",
                            backgroundRepeat: "no-repeat",
                            backgroundSize: "cover",
                        }}
                    >
                        <Card sx={{ minWidth: 300 }}>
                            <Box
                                sx={{
                                    margin: "1em",
                                    display: "flex",
                                    justifyContent: "center",
                                }}
                            >
                                <Avatar sx={{ bgcolor: "primary.main" }}>
                                    <LockIcon />
                                </Avatar>
                            </Box>
                            <Box sx={{ padding: "0 1em 1em 1em" }}>
                                <Box sx={{ marginTop: "1em" }}>
                                    <TextInput
                                        autoFocus
                                        source="username"
                                        label="Username"
                                        disabled={loading}
                                        validate={required()}
                                        fullWidth
                                    />
                                </Box>
                                <Box sx={{ marginTop: "1em" }}>
                                    <TextInput
                                        source="password"
                                        label="Password"
                                        type="password"
                                        disabled={loading}
                                        validate={required()}
                                        fullWidth
                                    />
                                </Box>
                            </Box>
                            <CardActions sx={{ padding: "0 1em 1em 1em" }}>
                                <Stack spacing={2} sx={{ width: "100%" }}>
                                    <Button
                                        variant="contained"
                                        type="submit"
                                        color="primary"
                                        disabled={loading}
                                        fullWidth
                                        startIcon={<PersonIcon />}
                                    >
                                        {loading && <CircularProgress size={25} thickness={2} />}
                                        Sign in with user
                                    </Button>
                                    {window.__RUNTIME_CONFIG__.OIDC_ENABLE == "true" && <OIDCSignInButton />}
                                </Stack>
                            </CardActions>
                        </Card>
                    </Box>
                </Form>
            )}
        </Fragment>
    );
};

Login.propTypes = {
    authProvider: PropTypes.func,
    previousRoute: PropTypes.string,
};

export default Login;

interface FormValues {
    username?: string;
    password?: string;
}
