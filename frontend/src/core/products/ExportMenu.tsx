import { faFileCsv, faFileExcel } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import DownloadIcon from "@mui/icons-material/Download";
import ViewQuiltIcon from "@mui/icons-material/ViewQuilt";
import { ListItemIcon } from "@mui/material";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Fragment, MouseEvent, useState } from "react";
import { useNotify } from "react-admin";

import axios_instance from "../../access_control/axios_instance";
import { getIconAndFontColor } from "../../commons/functions";

interface ExportMenuProps {
    product: any;
    is_product_group: boolean;
}

const ExportMenu = (props: ExportMenuProps) => {
    const notify = useNotify();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const exportDataCsv = async (url: string, filename: string, message: string) => {
        axios_instance
            .get(url)
            .then(function (response) {
                const blob = new Blob([response.data], { type: "text/csv" });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = filename;
                link.click();

                notify(message + " downloaded", {
                    type: "success",
                });
            })
            .catch(function (error) {
                notify(error.message, {
                    type: "warning",
                });
            });
        handleClose();
    };

    const exportDataExcel = async (url: string, filename: string, message: string) => {
        axios_instance
            .get(url, {
                responseType: "arraybuffer",
                headers: { Accept: "*/*" },
            })
            .then(function (response) {
                const blob = new Blob([response.data], {
                    type: "application/zip",
                });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = filename;
                link.click();

                notify(message + " downloaded", {
                    type: "success",
                });
            })
            .catch(function (error) {
                notify(error.message, {
                    type: "warning",
                });
            });
        handleClose();
    };

    const exportCodeChartaMetrics = async () => {
        exportDataCsv(
            "/metrics/export_codecharta?product_id=" + props.product.id,
            "secobserve_codecharta_metrics.csv",
            "CodeCharta metrics"
        );
    };

    const exportAllObservationsExcel = async () => {
        exportDataExcel(
            "/products/" + props.product.id + "/export_observations_excel/",
            "all_observations.xlsx",
            "Observations"
        );
    };

    const exportOpenObservationsExcel = async () => {
        exportDataExcel(
            "/products/" + props.product.id + "/export_observations_excel/?status=Open",
            "open_observations.xlsx",
            "Observations"
        );
    };

    const exportAllObservationsCsv = async () => {
        exportDataCsv(
            "/products/" + props.product.id + "/export_observations_csv/",
            "all_observations.csv",
            "Observations"
        );
    };

    const exportOpenObservationsCsv = async () => {
        exportDataCsv(
            "/products/" + props.product.id + "/export_observations_csv/?status=Open",
            "open_observations.csv",
            "Observations"
        );
    };

    const exportMetricsExcel = async () => {
        exportDataExcel(
            "/metrics/export_excel?product_id=" + props.product.id,
            "product_metrics.xlsx",
            "Product Metrics"
        );
    };

    const exportMetricsCsv = async () => {
        exportDataCsv("/metrics/export_csv?product_id=" + props.product.id, "product_metrics.csv", "Product Metrics");
    };

    return (
        <Fragment>
            <Button
                id="export-button"
                aria-controls={open ? "export-menu" : undefined}
                aria-haspopup="true"
                aria-expanded={open ? "true" : undefined}
                onClick={handleClick}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<DownloadIcon />}
            >
                Export
            </Button>
            <Menu
                id="basic-menu"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                MenuListProps={{
                    "aria-labelledby": "basic-button",
                }}
            >
                <MenuItem onClick={exportOpenObservationsExcel}>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileExcel} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    Open observations / Excel
                </MenuItem>
                <MenuItem onClick={exportOpenObservationsCsv} divider>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileCsv} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    Open observations / CSV
                </MenuItem>
                <MenuItem onClick={exportAllObservationsExcel}>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileExcel} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    All observations / Excel
                </MenuItem>
                <MenuItem onClick={exportAllObservationsCsv} divider>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileCsv} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    All observations / CSV
                </MenuItem>
                <MenuItem onClick={exportMetricsExcel}>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileExcel} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    Metrics / Excel
                </MenuItem>
                <MenuItem onClick={exportMetricsCsv} divider={!props.is_product_group}>
                    <ListItemIcon>
                        <FontAwesomeIcon icon={faFileCsv} color={getIconAndFontColor()} />
                    </ListItemIcon>
                    Metrics / CSV
                </MenuItem>
                {!props.is_product_group && (
                    <MenuItem onClick={exportCodeChartaMetrics}>
                        <ListItemIcon>
                            <ViewQuiltIcon sx={{ color: getIconAndFontColor() }} />
                        </ListItemIcon>
                        CodeCharta metrics
                    </MenuItem>
                )}
            </Menu>
        </Fragment>
    );
};

export default ExportMenu;
