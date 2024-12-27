import CancelIcon from "@mui/icons-material/Cancel";
import { Button } from "@mui/material";

interface CancelButtonProps {
    onClick: () => void;
}

const CancelButton = ({ onClick }: CancelButtonProps) => (
    <Button
        sx={{
            mr: "1em",
            direction: "row",
            justifyContent: "center",
            alignItems: "center",
        }}
        variant="contained"
        onClick={onClick}
        color="inherit"
        startIcon={<CancelIcon />}
    >
        Cancel
    </Button>
);

export default CancelButton;
