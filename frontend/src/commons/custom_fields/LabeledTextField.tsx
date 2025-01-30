import { Typography } from "@mui/material";

interface LabeledTextFieldProps {
    text: string | number;
    label: string;
}

const LabeledTextField = (props: LabeledTextFieldProps) => {
    return <Typography variant="body2">{props.text}</Typography>;
};

export default LabeledTextField;
