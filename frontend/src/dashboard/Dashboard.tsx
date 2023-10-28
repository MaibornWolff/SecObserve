import { Stack, Typography } from "@mui/material";
import React from "react";
import { useAuth } from "react-oidc-context";

import { jwt_signed_in } from "../access_control/authProvider";
import ObservationDashboardList from "../core/observations/ObservationDashboardList";
import MetricsHeader from "../metrics/MetricsHeader";
import MetricsSeveritiesCurrent from "../metrics/MetricsSeveritiesCurrent";
import MetricsSeveritiesTimeline from "../metrics/MetricsSeveritiesTimeLine";
import MetricsStatusCurrent from "../metrics/MetricsStatusCurrent";

const Dashboard = () => {
    const auth = useAuth();

    return (
        (jwt_signed_in() || auth.isAuthenticated) && (
            <React.Fragment>
                <MetricsHeader repository_default_branch={undefined} />
                <Stack
                    direction="row"
                    spacing={2}
                    sx={{
                        alignItems: "top",
                        marginTop: 2,
                    }}
                >
                    <MetricsSeveritiesCurrent product_id={undefined} />
                    <MetricsSeveritiesTimeline product_id={undefined} />
                    <MetricsStatusCurrent product_id={undefined} />
                </Stack>
                <Typography variant="h6" sx={{ marginTop: 4, marginBottom: 2 }}>
                    Open observations of the last 7 days
                </Typography>
                <ObservationDashboardList />
            </React.Fragment>
        )
    );
};

export default Dashboard;
