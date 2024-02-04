import { Stack } from "@mui/material";
import { Fragment } from "react";
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
            <Fragment>
                <MetricsHeader repository_default_branch={undefined} on_dashboard={true} />
                <Stack
                    direction="row"
                    spacing={2}
                    sx={{
                        alignItems: "top",
                        marginTop: 2,
                    }}
                >
                    <MetricsSeveritiesCurrent product_id={undefined} on_dashboard={true} />
                    <MetricsSeveritiesTimeline product_id={undefined} on_dashboard={true} />
                    <MetricsStatusCurrent product_id={undefined} on_dashboard={true} />
                </Stack>
                <ObservationDashboardList />
            </Fragment>
        )
    );
};

export default Dashboard;
