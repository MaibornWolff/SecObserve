import CancelIcon from "@mui/icons-material/Cancel";
import { Button } from "@mui/material";

interface CancelButtonProps {
    onClick: () => void;
}

const CancelButton = ({ onClick }: CancelButtonProps) => (
    <Button sx={{ mr: "1em" }} variant="contained" onClick={onClick} color="inherit" startIcon={<CancelIcon />}>
        Cancel
    </Button>
);

export default CancelButton;
