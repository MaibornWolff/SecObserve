import { Paper } from "@mui/material";
import {
    CategoryScale,
    Chart as ChartJS,
    Filler,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
} from "chart.js";
import { get } from "http";
import { useState } from "react";
import { Identifier, useNotify } from "react-admin";
import { Line } from "react-chartjs-2";

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

interface ProductMetricsSeveritiesProps {
    product_id: Identifier | undefined;
}

const ProductMetricsSeverities = (props: ProductMetricsSeveritiesProps) => {
    const [datasets, setDatasets] = useState<any[]>([]);
    const [loaded, setLoaded] = useState(false);
    const [loading, setLoading] = useState(false);
    const notify = useNotify();

    const days = [
        new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        new Date(Date.now()).toLocaleDateString(),
    ];

    function get_metrics(date: Date, metrics_data: any) {
        const date_string = date.toISOString().split("T")[0];
        const metrics = metrics_data[date_string];
        if (metrics) {
            return metrics;
        } else {
            return {
                open_critical: 0,
                open_high: 0,
                open_medium: 0,
                open_low: 0,
                open_none: 0,
                open_unkown: 0,
            };
        }
    }

    const chart_data = {
        labels: days,
        datasets: datasets,
    };

    function get_data() {
        setLoading(true);

        let url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/metrics/product_metrics_counts/?age=Past%207%20days";
        if (props.product_id) {
            url += "&product_id=" + props.product_id;
        }

        httpClient(url, {
            method: "GET",
        }).then((result) => {
            const critical_observations = [];
            const high_observations = [];
            const medium_observations = [];
            const low_observations = [];
            const none_observations = [];
            const unkown_observations = [];

            let metrics = get_metrics(new Date(Date.now() - 6 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            metrics = get_metrics(new Date(Date.now()), result.json);
            critical_observations.push(metrics.open_critical);
            high_observations.push(metrics.open_high);
            medium_observations.push(metrics.open_medium);
            low_observations.push(metrics.open_low);
            none_observations.push(metrics.open_none);
            unkown_observations.push(metrics.open_unkown);

            const data_sets = [
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_UNKOWN,
                    data: unkown_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_UNKOWN),
                    cubicInterpolationMode: "monotone",
                },
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_NONE,
                    data: none_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_NONE),
                    cubicInterpolationMode: "monotone",
                },
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_LOW,
                    data: low_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_LOW),
                    cubicInterpolationMode: "monotone",
                },
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_MEDIUM,
                    data: medium_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_MEDIUM),
                    cubicInterpolationMode: "monotone",
                },
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_HIGH,
                    data: high_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_HIGH),
                    cubicInterpolationMode: "monotone",
                },
                {
                    fill: true,
                    label: OBSERVATION_SEVERITY_CRITICAL,
                    data: critical_observations,
                    borderColor: "#ffffff",
                    backgroundColor: get_severity_color(OBSERVATION_SEVERITY_CRITICAL),
                    cubicInterpolationMode: "monotone",
                },
            ];
            setDatasets(data_sets);
        });
        setLoaded(true);
        setLoading(false);
    }

    if (!loaded) {
        get_data();
    }

    ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler, Legend);

    return (
        <Paper
            sx={{
                alignItems: "top",
                display: "flex",
                justifyContent: "flex-center",
                width: "33%",
            }}
        >
            {!loading && (
                <Line
                    width="50vw"
                    height="50vw"
                    data={chart_data}
                    options={{
                        scales: {
                            y: {
                                stacked: true,
                            },
                        },
                        borderColor: getBackgroundColor(),
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: "Severities of open observations (last 7 days)",
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

export default ProductMetricsSeverities;
