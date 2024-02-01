import ArticleIcon from "@mui/icons-material/Article";
import SettingsIcon from "@mui/icons-material/Settings";
import { Box, Divider, ListItemIcon, ListItemText, MenuItem, Theme, Typography, useMediaQuery } from "@mui/material";
import { forwardRef } from "react";
import { AppBar, Logout, UserMenu, useUserMenu } from "react-admin";
import { Link } from "react-router-dom";

import About from "../about/About";
import Logo from "./Logo";

const DocumentationMenu = forwardRef(() => {
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
                <ArticleIcon />
            </ListItemIcon>
            <ListItemText>Documentation</ListItemText>
        </MenuItem>
    );
});

const SettingsMenu = forwardRef(() => {
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
            <SettingsMenu />
            <Divider />
            <DocumentationMenu />
            <About />
            <Divider />
            <Logout />
        </UserMenu>
    );
};

const CustomAppBar = () => {
    const isLargeEnough = useMediaQuery<Theme>((theme) => theme.breakpoints.up("sm"));
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
