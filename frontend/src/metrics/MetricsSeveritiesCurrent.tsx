import { Paper } from "@mui/material";
import { ArcElement, Chart as ChartJS, Legend, RadialLinearScale, Title, Tooltip } from "chart.js";
import { useState } from "react";
import { Identifier, useNotify } from "react-admin";
import { PolarArea } from "react-chartjs-2";

import { get_severity_color } from "../commons/functions";
import { httpClient } from "../commons/ra-data-django-rest-framework";
import {
    OBSERVATION_SEVERITY_CRITICAL,
    OBSERVATION_SEVERITY_HIGH,
    OBSERVATION_SEVERITY_LOW,
    OBSERVATION_SEVERITY_MEDIUM,
    OBSERVATION_SEVERITY_NONE,
    OBSERVATION_SEVERITY_UNKOWN,
} from "../core/types";
import { getBackgroundColor, getElevation, getFontColor, getGridColor } from "./functions";

interface MetricsSeveritiesCurrentProps {
    product_id: Identifier | undefined;
    on_dashboard?: boolean;
}

const MetricsSeveritiesCurrent = (props: MetricsSeveritiesCurrentProps) => {
    const [data, setData] = useState<number[]>([]);
    const [loaded, setLoaded] = useState(false);
    const [loading, setLoading] = useState(false);
    const notify = useNotify();

    const chart_data = {
        labels: [
            OBSERVATION_SEVERITY_CRITICAL,
            OBSERVATION_SEVERITY_HIGH,
            OBSERVATION_SEVERITY_MEDIUM,
            OBSERVATION_SEVERITY_LOW,
            OBSERVATION_SEVERITY_NONE,
            OBSERVATION_SEVERITY_UNKOWN,
        ],
        datasets: [
            {
                label: "Severities of open observations",
                data: data,
                backgroundColor: [
                    get_severity_color(OBSERVATION_SEVERITY_CRITICAL),
                    get_severity_color(OBSERVATION_SEVERITY_HIGH),
                    get_severity_color(OBSERVATION_SEVERITY_MEDIUM),
                    get_severity_color(OBSERVATION_SEVERITY_LOW),
                    get_severity_color(OBSERVATION_SEVERITY_NONE),
                    get_severity_color(OBSERVATION_SEVERITY_UNKOWN),
                ],
            },
        ],
    };

    function get_data() {
        setLoading(true);

        let url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/metrics/product_metrics_current/";
        if (props.product_id) {
            url += "?product_id=" + props.product_id;
        }

        httpClient(url, {
            method: "GET",
        })
            .then((result) => {
                const new_data = [
                    result.json.open_critical,
                    result.json.open_high,
                    result.json.open_medium,
                    result.json.open_low,
                    result.json.open_none,
                    result.json.open_unknown,
                ];
                setData((data) => data.concat(new_data));
            })
            .catch((error) => {
                if (error !== undefined) {
                    notify(error.message, {
                        type: "warning",
                    });
                } else {
                    notify("Error while loading metrics", {
                        type: "warning",
                    });
                }
            });
        setLoaded(true);
        setLoading(false);
    }

    if (!loaded) {
        get_data();
    }

    ChartJS.register(Title, Legend, RadialLinearScale, ArcElement, Tooltip);

    return (
        <Paper
            elevation={getElevation(props.on_dashboard)}
            sx={{
                alignItems: "center",
                display: "flex",
                justifyContent: "flex-center",
                width: "33%",
            }}
        >
            {!loading && (
                <PolarArea
                    data={chart_data}
                    options={{
                        borderColor: getBackgroundColor(),
                        scales: {
                            r: {
                                display: true,
                                grid: {
                                    circular: true,
                                    color: getGridColor(),
                                },
                                ticks: {
                                    backdropColor: getBackgroundColor(),
                                    color: getFontColor(),
                                },
                            },
                            rAxes: {
                                display: false,
                            },
                        },
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: "Severities of open observations (current)",
                                color: getFontColor(),
                            },
                            legend: {
                                display: true,
                                position: "bottom",
                                labels: {
                                    color: getFontColor(),
                                },
                            },
                        },
                    }}
                />
            )}
        </Paper>
    );
};

export default MetricsSeveritiesCurrent;
