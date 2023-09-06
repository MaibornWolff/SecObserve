import { faMicrosoft } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "@mui/material";
import { useAuth } from "react-oidc-context";

export const OAuth2SignInButton = () => {
    const auth = useAuth();

    const handleLogin = () => {
        auth.signinRedirect();
    };
    return (
        <Button
            variant="contained"
            onClick={() => handleLogin()}
            startIcon={<FontAwesomeIcon icon={faMicrosoft} color={"white"} />}
        >
            Sign in with OAuth2
        </Button>
    );
};
