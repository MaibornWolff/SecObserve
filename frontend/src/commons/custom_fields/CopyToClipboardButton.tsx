import { Button } from "@mui/material";
import { useNotify } from "react-admin";

type CopyToClipboardButtonProps = {
    text: string;
};

const CopyToClipboardButton = (props: CopyToClipboardButtonProps) => {
    const notify = useNotify();
    const handleClick = () => {
        navigator.clipboard.writeText(props.text);
        notify("Product API token copied to clipboard");
    };

    return (
        <Button onClick={handleClick} variant="contained">
            Copy
        </Button>
    );
};

export default CopyToClipboardButton;
