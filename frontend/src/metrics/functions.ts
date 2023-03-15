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
        return "#1e1e1e";
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
