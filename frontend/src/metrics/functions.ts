import { getSettingTheme } from "../commons/settings/functions";

export function getGridColor() {
    if (getSettingTheme() == "dark") {
        return "#666666";
    } else {
        return "#e5e5e5";
    }
}

export function getBackgroundColor() {
    if (getSettingTheme() == "dark") {
        return "#282828";
    } else {
        return "white";
    }
}

export function getFontColor() {
    if (getSettingTheme() == "dark") {
        return "#bcbcbc";
    } else {
        return "#666666";
    }
}

export function getElevation(on_dashboard?: boolean) {
    if (on_dashboard) {
        return 1;
    }

    if (getSettingTheme() == "dark") {
        return 4;
    } else {
        return 1;
    }
}
