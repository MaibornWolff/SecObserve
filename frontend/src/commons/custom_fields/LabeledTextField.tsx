import LaunchIcon from "@mui/icons-material/Launch";

import { useStyles } from "../../commons/layout/themes";

interface LabeledTextFieldProps {
    text: string | number;
    label: string;
}

const LabeledTextField = (props: LabeledTextFieldProps) => {
    const { classes } = useStyles();

    return (
        <div
            style={{
                fontSize: "0.875rem",
                fontFamily: "Roboto",
                lineHeight: 1.43,
            }}
        >
            {props.text}
        </div>
    );
};

LabeledTextField.defaultProps = { label: "" };

export default LabeledTextField;
