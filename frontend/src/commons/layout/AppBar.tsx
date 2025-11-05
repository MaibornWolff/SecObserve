import ArticleIcon from "@mui/icons-material/Article";
import PersonIcon from "@mui/icons-material/Person";
import SettingsIcon from "@mui/icons-material/Settings";
import { Box, Divider, ListItemIcon, ListItemText, MenuItem, Theme, Typography, useMediaQuery } from "@mui/material";
import { forwardRef } from "react";
import { AppBar, LoadingIndicator, Logout, UserMenu, useUserMenu } from "react-admin";
import { Link } from "react-router-dom";

import About from "../about/About";
import Logo from "./Logo";
import ToggleThemeButton from "./ToggleThemeButton";

const DocumentationMenu = forwardRef(() => {
    const userMenuContext = useUserMenu();
    if (!userMenuContext) {
        return null;
    }
    const { onClose } = userMenuContext;

    return (
        <MenuItem
            component="a"
            href="https://secobserve.github.io/SecObserve/"
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

const ProfileMenu = forwardRef(() => {
    const userMenuContext = useUserMenu();
    if (!userMenuContext) {
        return null;
    }
    const { onClose } = userMenuContext;

    const user = localStorage.getItem("user");
    const user_id = user ? JSON.parse(user).id : null;

    return (
        <MenuItem
            component={Link}
            to={"/users/" + user_id + "/show"}
            onClick={() => {
                localStorage.removeItem("userembeddedlist");
                localStorage.removeItem("useragembeddedlist");
                onClose();
            }}
        >
            <ListItemIcon>
                <PersonIcon />
            </ListItemIcon>
            <ListItemText>Profile</ListItemText>
        </MenuItem>
    );
});

const SettingsMenu = forwardRef(() => {
    const userMenuContext = useUserMenu();
    if (!userMenuContext) {
        return null;
    }
    const { onClose } = userMenuContext;

    return (
        <MenuItem
            component={Link}
            to="/user_settings"
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
            <ProfileMenu />
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
        <AppBar
            color="secondary"
            elevation={1}
            userMenu={<CustomUserMenu />}
            toolbar={
                <>
                    <ToggleThemeButton />
                    <LoadingIndicator />
                </>
            }
        >
            <Typography
                variant="h6"
                color="inherit"
                sx={{
                    flex: 1,
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                }}
            />
            {isLargeEnough && <Logo />}
            {isLargeEnough && <Box component="span" sx={{ flex: 1 }} />}
        </AppBar>
    );
};

export default CustomAppBar;
