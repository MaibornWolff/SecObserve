import AddIcon from "@mui/icons-material/Add";
import { Button } from "@mui/material";

interface AddButtonProps {
    title: string;
    onClick: () => void;
}

const AddButton = ({ title, onClick }: AddButtonProps) => {
    return (
        <Button
            variant="contained"
            onClick={onClick}
            sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem", marginBottom: 1 }}
            startIcon={<AddIcon />}
        >
            {title}
        </Button>
    );
};

export default AddButton;
