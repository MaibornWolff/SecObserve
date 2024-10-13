import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import { IconButton, Tooltip } from "@mui/material";
import { useTheme } from "react-admin";

import { getSettingTheme, saveSettingTheme } from "../../commons/user_settings/functions";

const tooltipTitle = () => {
    const theme = getSettingTheme();
    return theme === "dark" ? "Light mode" : "Dark mode";
};

const ThemeIcon = () => {
    const theme = getSettingTheme();
    return theme === "dark" ? (
        <LightModeIcon style={{ color: "rgba(255, 255, 255, 0.7)" }} />
    ) : (
        <DarkModeIcon style={{ color: "rgba(0, 0, 0, 0.54)" }} />
    );
};

const ToggleThemeButton = () => {
    const [, setTheme] = useTheme();

    const toogleTheme = () => {
        const theme = getSettingTheme();
        if (theme === "dark") {
            setTheme("light");
            localStorage.setItem("theme", "light");
            saveSettingTheme("light");
        } else {
            setTheme("dark");
            localStorage.setItem("theme", "dark");
            saveSettingTheme("dark");
        }
    };

    return (
        <Tooltip title={tooltipTitle()}>
            <IconButton onClick={toogleTheme}>
                <ThemeIcon />
            </IconButton>
        </Tooltip>
    );
};

export default ToggleThemeButton;
