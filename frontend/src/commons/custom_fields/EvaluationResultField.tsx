import { ChipField, useRecordContext } from "react-admin";

import {
    EVALUATION_RESULT_ALLOWED,
    EVALUATION_RESULT_FORBIDDEN,
    EVALUATION_RESULT_REVIEW_REQUIRED,
    EVALUATION_RESULT_UNKNOWN,
} from "../../licenses/types";

interface EvaluationResultProps {
    source: string;
    label: string;
}

function get_evaluation_result_color(record: any): string {
    let evaluation_result = "";
    if (record && record.component_license_data) {
        evaluation_result = record.component_license_data.evaluation_result;
    } else {
        evaluation_result = record.evaluation_result;
    }

    let backgroundColor = "transparent";
    switch (evaluation_result) {
        case EVALUATION_RESULT_ALLOWED:
            backgroundColor = "#53aa33";
            break;
        case EVALUATION_RESULT_FORBIDDEN:
            backgroundColor = "#df3d03";
            break;
        case EVALUATION_RESULT_REVIEW_REQUIRED:
            backgroundColor = "#f9a009";
            break;
        case EVALUATION_RESULT_UNKNOWN:
            backgroundColor = "rgba(255, 255, 255, 0.16)";
            break;
    }
    return backgroundColor;
}

export const EvaluationResultField = (props: EvaluationResultProps) => {
    const record = useRecordContext();
    return record ? (
        <ChipField
            source={props.source}
            sortable={true}
            sortBy={props.source}
            sx={{
                backgroundColor: get_evaluation_result_color(record),
                color: "white",
                width: "fit-content",
            }}
        />
    ) : null;
};
