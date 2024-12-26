import DeleteButton from "@mui/icons-material/Delete";
import { Button } from "@mui/material";

interface RemoveButtonProps {
    title: string;
    onClick: () => void;
}

const RemoveButton = ({ title, onClick }: RemoveButtonProps) => {
    return (
        <Button onClick={onClick} size="small" sx={{ padding: "0px", color: "#d32f2f" }} startIcon={<DeleteButton />}>
            {title}
        </Button>
    );
};

export default RemoveButton;
