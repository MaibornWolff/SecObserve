import { Paper } from "@mui/material";
import { Fragment } from "react";
import { useState } from "react";
import { Labeled, useNotify } from "react-admin";

import LabeledTextField from "../commons/custom_fields/LabeledTextField";
import { httpClient } from "../commons/ra-data-django-rest-framework";
import { getElevation } from "./functions";

interface MetricsHeaderProps {
    repository_default_branch: string | undefined;
    on_dashboard?: boolean;
}

const MetricsHeader = (props: MetricsHeaderProps) => {
    const [data, setData] = useState({
        last_calculated: new Date("2023-07-10T19:37:34.750324Z"),
        calculation_interval: 0,
    });
    const [loaded, setLoaded] = useState(false);
    const [loading, setLoading] = useState(false);
    const notify = useNotify();

    function get_data() {
        setLoading(true);

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/metrics/product_metrics_status/", {
            method: "GET",
        })
            .then((result) => {
                setData(result.json);
            })
            .catch((error) => {
                if (error !== undefined) {
                    notify(error.message, {
                        type: "warning",
                    });
                } else {
                    notify("Error while loading metrics status", {
                        type: "warning",
                    });
                }
            });
        setLoaded(true);
        setLoading(false);
    }

    function get_margin_left(repository_default_branch: string | undefined) {
        if (repository_default_branch) {
            return 8;
        }

        return 0;
    }

    const get_margin_top = (on_dashboard: boolean | undefined) => {
        if (on_dashboard) {
            return 2;
        }

        return 0;
    };

    if (!loaded) {
        get_data();
    }

    return (
        <Paper
            elevation={getElevation(props.on_dashboard)}
            sx={{
                alignItems: "top",
                display: "flex",
                justifyContent: "flex-start",
                padding: 2,
                marginTop: get_margin_top(props.on_dashboard),
            }}
        >
            {!loading && (
                <Fragment>
                    {props.repository_default_branch && (
                        <Labeled label="Default branch">
                            <LabeledTextField text={props.repository_default_branch} />
                        </Labeled>
                    )}
                    <Labeled
                        label="Metrics last calculated"
                        sx={{ marginLeft: get_margin_left(props.repository_default_branch) }}
                    >
                        <LabeledTextField text={new Date(data.last_calculated).toLocaleString()} />
                    </Labeled>
                    <Labeled label="Metrics calculation interval" sx={{ marginLeft: 8 }}>
                        <LabeledTextField text={data.calculation_interval + " minutes"} />
                    </Labeled>
                </Fragment>
            )}
        </Paper>
    );
};

export default MetricsHeader;
