import { ChipField, useRecordContext } from "react-admin";

import { get_evaluation_result_color } from "../functions";

interface EvaluationResultProps {
    source: string;
    label: string;
    sortable?: boolean;
}

export const EvaluationResultField = (props: EvaluationResultProps) => {
    const record = useRecordContext();
    return record ? (
        <ChipField
            source={props.source}
            sortable={props.sortable}
            sortBy={props.source}
            sx={{
                backgroundColor: get_evaluation_result_color(record, null),
                color: "white",
                width: "fit-content",
            }}
        />
    ) : null;
};
