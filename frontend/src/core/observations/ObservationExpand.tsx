import { Paper, Typography } from "@mui/material";
import { SimpleShowLayout, useRecordContext } from "react-admin";

import { getElevation } from "../../metrics/functions";
import ObservationShowDescriptionRecommendation from "./ObservationShowDescriptionRecommendation";
import ObservationShowOrigins from "./ObservationShowOrigins";

const ObservationExpand = () => {
    const observation = useRecordContext();
    return (
        <SimpleShowLayout>
            {observation && (observation.description || observation.recommendation) && (
                <Paper elevation={getElevation(false)} sx={{ marginBottom: 2, padding: 2 }}>
                    <Typography variant="h6">Observation</Typography>
                    <ObservationShowDescriptionRecommendation />
                </Paper>
            )}
            <ObservationShowOrigins showDependencies={false} elevated={false} />
        </SimpleShowLayout>
    );
};

export default ObservationExpand;
