import { Paper } from "@mui/material";
import { ArcElement, Chart as ChartJS, Legend, RadialLinearScale, Title, Tooltip } from "chart.js";
import { useState } from "react";
import { Identifier } from "react-admin";
import { PolarArea } from "react-chartjs-2";

import { httpClient } from "../commons/ra-data-django-rest-framework";
import {
    OBSERVATION_STATUS_DUPLICATE,
    OBSERVATION_STATUS_FALSE_POSITIVE,
    OBSERVATION_STATUS_IN_REVIEW,
    OBSERVATION_STATUS_NOT_AFFECTED,
    OBSERVATION_STATUS_NOT_SECURITY,
    OBSERVATION_STATUS_OPEN,
    OBSERVATION_STATUS_RESOLVED,
    OBSERVATION_STATUS_RISK_ACCEPTED,
} from "../core/types";
import { getBackgroundColor, getFontColor, getGridColor } from "./functions";

interface MetricStatusProps {
    product_id: Identifier | undefined;
}

const MetricStatus = (props: MetricStatusProps) => {
    const [data, setData] = useState<number[]>([]);
    const [loaded, setLoaded] = useState(false);
    const [loading, setLoading] = useState(false);

    const chart_data = {
        labels: [
            OBSERVATION_STATUS_OPEN,
            OBSERVATION_STATUS_RESOLVED,
            OBSERVATION_STATUS_DUPLICATE,
            OBSERVATION_STATUS_FALSE_POSITIVE,
            OBSERVATION_STATUS_IN_REVIEW,
            OBSERVATION_STATUS_NOT_AFFECTED,
            OBSERVATION_STATUS_NOT_SECURITY,
            OBSERVATION_STATUS_RISK_ACCEPTED,
        ],
        datasets: [
            {
                label: "Status of observations",
                data: data,
                backgroundColor: [
                    "#1f2c33",
                    "#3d5766",
                    "#79adcc",
                    "#bcb7b6",
                    "#ffc09f",
                    "#ffd799",
                    "#ffee93",
                    "#fcf5c7",
                ],
            },
        ],
    };

    function get_data() {
        setLoading(true);

        let url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/metrics/status_counts/";
        if (props.product_id) {
            url += "?product_id=" + props.product_id;
        }

        httpClient(url, {
            method: "GET",
        }).then((result) => {
            const new_data = [
                result.json.Open,
                result.json.Resolved,
                result.json.Duplicate,
                result.json[OBSERVATION_STATUS_FALSE_POSITIVE], // eslint-disable-line security/detect-object-injection
                result.json[OBSERVATION_STATUS_IN_REVIEW], // eslint-disable-line security/detect-object-injection
                result.json[OBSERVATION_STATUS_NOT_AFFECTED], // eslint-disable-line security/detect-object-injection
                result.json[OBSERVATION_STATUS_NOT_SECURITY], // eslint-disable-line security/detect-object-injection
                result.json[OBSERVATION_STATUS_RISK_ACCEPTED], // eslint-disable-line security/detect-object-injection
                // eslint is disabled because the values for the keys are constants
            ];
            setData((data) => data.concat(new_data));
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
                                text: "Status of observations",
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

export default MetricStatus;
