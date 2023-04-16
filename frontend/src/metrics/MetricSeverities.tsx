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
import { getBackgroundColor, getFontColor, getGridColor } from "./functions";

interface MetricSeveritiesProps {
    product_id: Identifier | undefined;
}

const MetricSeverities = (props: MetricSeveritiesProps) => {
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

        let url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/metrics/severity_counts/";
        if (props.product_id) {
            url += "?product_id=" + props.product_id;
        }

        httpClient(url, {
            method: "GET",
        })
            .then((result) => {
                localStorage.setItem("aad_login_finalized", "true");
                const new_data = [
                    result.json.Critical,
                    result.json.High,
                    result.json.Medium,
                    result.json.Low,
                    result.json.None,
                    result.json.Unkown,
                ];
                setData((data) => data.concat(new_data));
            })
            .catch((error) => {
                if (localStorage.getItem("aad_login_finalized") != "false") {
                    if (error !== undefined) {
                        notify(error.message, {
                            type: "warning",
                        });
                    } else {
                        notify("Error while loading metrics", {
                            type: "warning",
                        });
                    }
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
                                text: "Severities of open observations",
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

export default MetricSeverities;
