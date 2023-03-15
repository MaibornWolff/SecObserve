import { useRecordContext, ChipField } from "react-admin";
import { get_severity_color } from "../functions";

interface SeverityProps {
    source: string;
    sortable: boolean;
    label: string;
}

export const SeverityField = (props: SeverityProps) => {
    const record = useRecordContext();
    return record ? (
        <ChipField
            source={props.source}
            sortable={props.sortable}
            sortBy={props.source}
            sx={{
                backgroundColor: get_severity_color(record.current_severity),
                color: "white",
            }}
        />
    ) : null;
};

SeverityField.defaultProps = { label: "Severity", sortable: true };
