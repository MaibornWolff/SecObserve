import LoginIcon from "@mui/icons-material/Login";
import { Button } from "@mui/material";
import { useAuth } from "react-oidc-context";

export const OAuth2SignInButton = () => {
    const auth = useAuth();

    const handleLogin = () => {
        auth.signinRedirect();
    };
    return (
        <Button variant="contained" onClick={() => handleLogin()} startIcon={<LoginIcon />}>
            Enterprise Sign in
        </Button>
    );
};
