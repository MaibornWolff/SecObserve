import { useState } from "react";
import { useNotify } from "react-admin";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import DownloadIcon from "@mui/icons-material/Download";
import ViewQuiltIcon from "@mui/icons-material/ViewQuilt";
import { ListItemIcon } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFileExcel, faFileCsv } from "@fortawesome/free-solid-svg-icons";

import { getSettingTheme } from "../../commons/settings/functions";
import axios_instance from "../../access_control/axios_instance";

export default function ExportMenu(product: any) {
    const notify = useNotify();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    function getIconColor() {
        if (getSettingTheme() == "dark") {
            return "white";
        } else {
            return "black";
        }
    }
    const exportDataCsv = async (
        url_suffix: string,
        filename: string,
        message: string
    ) => {
        axios_instance
            .get("/products/" + product.product.id + url_suffix)
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

    const exportDataExcel = async (
        url_suffix: string,
        filename: string,
        message: string
    ) => {
        axios_instance
            .get("/products/" + product.product.id + url_suffix, {
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
            "/export_codecharta_metrics/",
            "secobserve_codecharta_metrics.csv",
            "CodeCharta metrics"
        );
    };

    const exportAllObservationsExcel = async () => {
        exportDataExcel(
            "/export_observations_excel/",
            "all_observations.xlsx",
            "Observations"
        );
    };

    const exportOpenObservationsExcel = async () => {
        exportDataExcel(
            "/export_observations_excel/?status=Open",
            "open_observations.xlsx",
            "Observations"
        );
    };

    const exportAllObservationsCsv = async () => {
        exportDataCsv(
            "/export_observations_csv/",
            "all_observations.csv",
            "Observations"
        );
    };

    const exportOpenObservationsCsv = async () => {
        exportDataCsv(
            "/export_observations_csv/?status=Open",
            "open_observations.csv",
            "Observations"
        );
    };

    return (
        <div>
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
                        <FontAwesomeIcon
                            icon={faFileExcel}
                            color={getIconColor()}
                        />
                    </ListItemIcon>
                    Open observations / Excel
                </MenuItem>
                <MenuItem onClick={exportOpenObservationsCsv} divider>
                    <ListItemIcon>
                        <FontAwesomeIcon
                            icon={faFileCsv}
                            color={getIconColor()}
                        />
                    </ListItemIcon>
                    Open observations / CSV
                </MenuItem>
                <MenuItem onClick={exportAllObservationsExcel}>
                    <ListItemIcon>
                        <FontAwesomeIcon
                            icon={faFileExcel}
                            color={getIconColor()}
                        />
                    </ListItemIcon>
                    All observations / Excel
                </MenuItem>
                <MenuItem onClick={exportAllObservationsCsv} divider>
                    <ListItemIcon>
                        <FontAwesomeIcon
                            icon={faFileCsv}
                            color={getIconColor()}
                        />
                    </ListItemIcon>
                    All observations / CSV
                </MenuItem>
                <MenuItem onClick={exportCodeChartaMetrics}>
                    <ListItemIcon>
                        <ViewQuiltIcon sx={{ color: getIconColor() }} />
                    </ListItemIcon>
                    CodeCharta metrics
                </MenuItem>
            </Menu>
        </div>
    );
}
