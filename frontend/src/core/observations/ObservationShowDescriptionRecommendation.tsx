import { Stack } from "@mui/material";
import { Labeled, useRecordContext } from "react-admin";

import MarkdownField from "../../commons/custom_fields/MarkdownField";

const ObservationShowDescriptionRecommendation = () => {
    const observation = useRecordContext();
    return (
        <Stack spacing={2}>
            {observation && observation.description != "" && (
                <Labeled>
                    <MarkdownField content={observation.description} label="Description" />
                </Labeled>
            )}
            {observation && observation.recommendation != "" && (
                <Labeled>
                    <MarkdownField content={observation.recommendation} label="Recommendation" />
                </Labeled>
            )}
        </Stack>
    );
};

export default ObservationShowDescriptionRecommendation;
