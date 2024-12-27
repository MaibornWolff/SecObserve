import { Button } from "@mui/material";

interface SmallButtonProps {
    title: string;
    onClick: () => void;
    icon: any;
}

const SmallButton = ({ title, onClick, icon }: SmallButtonProps) => {
    return (
        <Button onClick={onClick} size="small" sx={{ padding: "0px" }} startIcon={icon}>
            {title}
        </Button>
    );
};

export default SmallButton;
