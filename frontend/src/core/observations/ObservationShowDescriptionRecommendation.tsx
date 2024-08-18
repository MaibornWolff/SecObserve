import { Stack } from "@mui/material";
import { Labeled, useRecordContext } from "react-admin";

import MarkdownField from "../../commons/custom_fields/MarkdownField";

const ObservationShowDescriptionRecommendation = () => {
    const observation = useRecordContext();
    return (
        <Stack spacing={2}>
            {observation && observation.description != "" && (
                <Labeled label="Description" sx={{ paddingTop: 2 }}>
                    <MarkdownField content={observation.description} />
                </Labeled>
            )}
            {observation && observation.recommendation != "" && (
                <Labeled label="Recommendation">
                    <MarkdownField content={observation.recommendation} />
                </Labeled>
            )}
        </Stack>
    );
};

export default ObservationShowDescriptionRecommendation;
