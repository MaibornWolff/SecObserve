import * as React from "react";
import { Link } from "react-router-dom";
import { AppBar, Logout, UserMenu, useUserMenu } from "react-admin";
import {
    Box,
    Typography,
    useMediaQuery,
    Theme,
    MenuItem,
    ListItemIcon,
    ListItemText,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";
import SettingsIcon from "@mui/icons-material/Settings";

import Logo from "./Logo";

const DocumentationMenu = React.forwardRef(() => {
    const { onClose } = useUserMenu();

    return (
        <MenuItem
            component="a"
            href="https://maibornwolff.github.io/SecObserve/"
            target="_blank"
            rel="noreferrer"
            onClick={() => {
                onClose();
            }}
        >
            <ListItemIcon>
                <InfoIcon />
            </ListItemIcon>
            <ListItemText>Documentation</ListItemText>
        </MenuItem>
    );
});

const SettingsMenu = React.forwardRef(() => {
    const { onClose } = useUserMenu();

    return (
        <MenuItem
            component={Link}
            to="/settings"
            onClick={() => {
                onClose();
            }}
        >
            <ListItemIcon>
                <SettingsIcon />
            </ListItemIcon>
            <ListItemText>Settings</ListItemText>
        </MenuItem>
    );
});
const CustomUserMenu = () => {
    return (
        <UserMenu>
            <DocumentationMenu />
            <SettingsMenu />
            <Logout />
        </UserMenu>
    );
};

const CustomAppBar = () => {
    const isLargeEnough = useMediaQuery<Theme>((theme) =>
        theme.breakpoints.up("sm")
    );
    return (
        <AppBar color="secondary" elevation={1} userMenu={<CustomUserMenu />}>
            <Typography
                variant="h6"
                color="inherit"
                sx={{
                    flex: 1,
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                }}
                id="react-admin-title"
            />
            {isLargeEnough && <Logo />}
            {isLargeEnough && <Box component="span" sx={{ flex: 1 }} />}
        </AppBar>
    );
};

export default CustomAppBar;
