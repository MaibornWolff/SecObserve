import { ChipField, useRecordContext } from "react-admin";

import { get_severity_color } from "../functions";

interface SeverityProps {
    source: string;
    sortable: boolean;
    label: string;
}

function get_current_severity(record: any) {
    if (record.current_severity !== undefined) {
        return record.current_severity;
    } else if (
        record.potential_duplicate_observation !== undefined &&
        record.potential_duplicate_observation.current_severity !== undefined
    ) {
        return record.potential_duplicate_observation.current_severity;
    } else if (record.issue_tracker_minimum_severity !== undefined) {
        return record.issue_tracker_minimum_severity;
    } else {
        return null;
    }
}

export const SeverityField = (props: SeverityProps) => {
    const record = useRecordContext();
    return record ? (
        <ChipField
            source={props.source}
            sortable={props.sortable}
            sortBy={props.source}
            sx={{
                backgroundColor: get_severity_color(get_current_severity(record)),
                color: "white",
                width: "fit-content",
            }}
        />
    ) : null;
};

SeverityField.defaultProps = { label: "Severity", sortable: true };
