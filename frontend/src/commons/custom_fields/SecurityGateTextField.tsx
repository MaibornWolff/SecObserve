import { ChipField, useRecordContext } from "react-admin";

interface SecurityGateTextProps {
    label: string;
}

export const SecurityGateTextField = (props: SecurityGateTextProps) => {
    const record = useRecordContext();

    function get_severity_color() {
        if (record?.security_gate_passed) {
            return "#0a0";
        } else {
            return "#d4333f";
        }
    }

    function get_text_record() {
        if (record?.security_gate_passed) {
            return { text: "Passed" };
        } else {
            return { text: "Failed" };
        }
    }

    return record?.security_gate_passed != null ? (
        <ChipField
            label={props.label}
            source="text"
            record={get_text_record()}
            sortable={true}
            sortBy="security_gate_passed"
            sx={{
                backgroundColor: get_severity_color(),
                color: "white",
            }}
        />
    ) : null;
};
