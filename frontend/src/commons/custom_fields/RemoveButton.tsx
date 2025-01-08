import DeleteButton from "@mui/icons-material/Delete";
import { Button } from "@mui/material";

interface RemoveButtonProps {
    title: string;
    onClick: () => void;
}

const RemoveButton = ({ title, onClick }: RemoveButtonProps) => {
    return (
        <Button
            onClick={onClick}
            size="small"
            sx={{ paddingTop: 0, paddingBottom: 0, paddingLeft: "5px", paddingRight: "5px", color: "#d32f2f" }}
            startIcon={<DeleteButton />}
        >
            {title}
        </Button>
    );
};

export default RemoveButton;
