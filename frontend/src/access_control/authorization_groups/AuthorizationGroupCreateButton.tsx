import AddIcon from "@mui/icons-material/Add";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";

const AuthorizationGroupCreateButton = () => {
    return (
        <Button
            variant="contained"
            sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
            startIcon={<AddIcon />}
            component={Link}
            to={"/authorization_groups/create"}
        >
            Add authorization group
        </Button>
    );
};

export default AuthorizationGroupCreateButton;
