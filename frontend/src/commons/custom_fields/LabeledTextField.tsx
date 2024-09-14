interface LabeledTextFieldProps {
    text: string | number;
    label: string;
}

const LabeledTextField = (props: LabeledTextFieldProps) => {
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

export default LabeledTextField;
