import AddIcon from "@mui/icons-material/Add";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";

interface CreateButtonProps {
    title: string;
    to: string;
}

const CreateButton = ({ title, to }: CreateButtonProps) => {
    return (
        <Button
            variant="contained"
            sx={{ width: "fit-content", fontSize: "0.8125rem" }}
            startIcon={<AddIcon />}
            component={Link}
            to={to}
        >
            {title}
        </Button>
    );
};

export default CreateButton;
