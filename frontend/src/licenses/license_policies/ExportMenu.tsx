import DescriptionIcon from "@mui/icons-material/Description";
import DownloadIcon from "@mui/icons-material/Download";
import { ListItemIcon } from "@mui/material";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Fragment, MouseEvent, useState } from "react";
import { useNotify } from "react-admin";

import axios_instance from "../../access_control/auth_provider/axios_instance";
import { getIconAndFontColor } from "../../commons/functions";

interface ExportMenuProps {
    license_policy: any;
}

const ExportMenu = ({ license_policy }: ExportMenuProps) => {
    const notify = useNotify();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const exportLicensePolicyJSON = async () => {
        exportLicensePolicy("json");
    };

    const exportLicensePolicyYAML = async () => {
        exportLicensePolicy("yaml");
    };

    const exportLicensePolicy = async (format: string) => {
        axios_instance
            .get("/license_policies/" + license_policy.id + "/export_" + format + "/")
            .then(function (response) {
                let blob = new Blob([response.data], { type: "application/" + format });
                if (format === "json") {
                    blob = new Blob([JSON.stringify(response.data, null, 4)], { type: "application/" + format });
                }
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = "license_policy_" + license_policy.id + "." + format;
                link.click();

                notify("License Policy downloaded", {
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

    return (
        <Fragment>
            <Button
                id="export-button"
                aria-controls={open ? "export-menu" : undefined}
                aria-haspopup="true"
                aria-expanded={open ? "true" : undefined}
                onClick={handleClick}
                size="small"
                sx={{ padding: "0px" }}
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
                <MenuItem onClick={exportLicensePolicyJSON}>
                    <ListItemIcon>
                        <DescriptionIcon sx={{ color: getIconAndFontColor() }} />
                    </ListItemIcon>
                    JSON
                </MenuItem>
                <MenuItem onClick={exportLicensePolicyYAML}>
                    <ListItemIcon>
                        <DescriptionIcon sx={{ color: getIconAndFontColor() }} />
                    </ListItemIcon>
                    YAML
                </MenuItem>
            </Menu>
        </Fragment>
    );
};

export default ExportMenu;
