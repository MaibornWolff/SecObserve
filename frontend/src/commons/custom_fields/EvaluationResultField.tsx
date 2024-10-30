import { ChipField, useRecordContext } from "react-admin";

import { get_evaluation_result_color } from "../functions";

interface EvaluationResultProps {
    source: string;
    label: string;
}

export const EvaluationResultField = (props: EvaluationResultProps) => {
    const record = useRecordContext();
    return record ? (
        <ChipField
            source={props.source}
            sortable={true}
            sortBy={props.source}
            sx={{
                backgroundColor: get_evaluation_result_color(record, null),
                color: "white",
                width: "fit-content",
            }}
        />
    ) : null;
};
