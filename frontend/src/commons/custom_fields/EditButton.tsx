import EditIcon from "@mui/icons-material/Edit";
import { Button } from "@mui/material";

interface EditButtonProps {
    title: string;
    onClick: () => void;
}

const EditButton = ({ title, onClick }: EditButtonProps) => {
    return (
        <Button onClick={onClick} size="small" sx={{ padding: "0px" }} startIcon={<EditIcon />}>
            {title}
        </Button>
    );
};

export default EditButton;
