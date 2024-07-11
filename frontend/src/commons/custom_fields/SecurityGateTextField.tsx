import { ChipField, useRecordContext } from "react-admin";

interface SecurityGateTextProps {
    sortable: boolean;
    label: string;
}

export const SecurityGateTextField = (props: SecurityGateTextProps) => {
    const record = useRecordContext();

    function get_severity_color() {
        if (record && record.security_gate_passed) {
            return "#0a0";
        } else {
            return "#d4333f";
        }
    }

    function get_text_record() {
        if (record && record.security_gate_passed) {
            return { text: "Passed" };
        } else {
            return { text: "Failed" };
        }
    }

    return record && record.security_gate_passed != null ? (
        <ChipField
            source="text"
            record={get_text_record()}
            sortable={props.sortable}
            sortBy="security_gate_passed"
            sx={{
                backgroundColor: get_severity_color(),
                color: "white",
            }}
        />
    ) : null;
};

SecurityGateTextField.defaultProps = { label: "Security gate", sortable: true };
