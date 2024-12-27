import { Button } from "@mui/material";

interface SmallButtonProps {
    title: string;
    onClick: () => void;
    icon: any;
}

const SmallButton = ({ title, onClick, icon }: SmallButtonProps) => {
    return (
        <Button
            onClick={onClick}
            size="small"
            sx={{ paddingTop: 0, paddingBottom: 0, paddingLeft: "5px", paddingRight: "5px" }}
            startIcon={icon}
        >
            {title}
        </Button>
    );
};

export default SmallButton;
