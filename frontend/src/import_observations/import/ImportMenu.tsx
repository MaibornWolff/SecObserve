import UploadIcon from "@mui/icons-material/Upload";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { Fragment, MouseEvent, useState } from "react";

import ApiImportObservations from "./ApiImportObservations";
import FileUploadObservations from "./FileUploadObservations";

interface ImportMenuProps {
    product: any;
}

const ImportMenu = (props: ImportMenuProps) => {
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <Fragment>
            <Button
                id="import-button"
                aria-controls={open ? "import-menu" : undefined}
                aria-haspopup="true"
                aria-expanded={open ? "true" : undefined}
                onClick={handleClick}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<UploadIcon />}
            >
                import
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
                <MenuItem onKeyDown={(e) => e.stopPropagation()}>
                    <FileUploadObservations />
                </MenuItem>
                <MenuItem onKeyDown={(e) => e.stopPropagation()}>
                    <ApiImportObservations product={props.product} />
                </MenuItem>
            </Menu>
        </Fragment>
    );
};

export default ImportMenu;
