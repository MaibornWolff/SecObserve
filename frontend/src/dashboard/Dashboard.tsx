import React from "react";
import { Stack, Typography } from "@mui/material";

import MetricSeverities from "../metrics/MetricSeverities";
import MetricStatus from "../metrics/MetricStatus";
import ObservationDashboardList from "../core/observations/ObservationDashboardList";

const Dashboard = () => {
    return (
        <React.Fragment>
            <Stack
                direction="row"
                spacing={2}
                sx={{
                    alignItems: "center",
                    marginTop: 2,
                }}
            >
                <MetricSeverities product_id={undefined} />
                <MetricStatus product_id={undefined} />
            </Stack>
            <Typography variant="h6" sx={{ marginTop: 4, marginBottom: 2 }}>
                Open observations of the last 7 days
            </Typography>
            <ObservationDashboardList />
        </React.Fragment>
    );
};

export default Dashboard;
