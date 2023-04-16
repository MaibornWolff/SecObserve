import { useMsal } from "@azure/msal-react";
import { faMicrosoft } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button } from "@mui/material";
import { useNotify } from "react-admin";

import { loginRequest } from "./aad";

export const AADSignInButton = () => {
    const { instance } = useMsal();
    const notify = useNotify();

    const handleLogin = (loginType: string) => {
        localStorage.setItem("aad_login_finalized", "false");
        if (loginType === "redirect") {
            instance.loginRedirect(loginRequest).catch((error) => {
                notify(error.message, { type: "warning" });
            });
        }
        if (loginType === "popup") {
            instance.loginPopup(loginRequest).catch((error) => {
                notify(error.message, { type: "warning" });
            });
        }
    };
    return (
        <Button
            variant="contained"
            onClick={() => handleLogin("redirect")}
            startIcon={<FontAwesomeIcon icon={faMicrosoft} color={"white"} />}
        >
            Sign in with Microsoft
        </Button>
    );
};
