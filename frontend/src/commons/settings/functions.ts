import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { darkTheme, lightTheme } from "../layout/themes";

export async function saveSettingTheme(theme: string) {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    user.setting_theme = theme;
    localStorage.setItem("user", JSON.stringify(user));
    saveSetting({ setting_theme: theme });
}

export function getSettingTheme(): string {
    let theme = "light";

    const user = localStorage.getItem("user");
    if (user) {
        const user_json = JSON.parse(user);
        theme = user_json.setting_theme;
    }

    return theme;
}

export function saveSettingListSize(list_size: string) {
    saveSetting({ setting_list_size: list_size });
}

export function getSettingListSize(): "small" | "medium" | undefined {
    let list_size: "small" | "medium" | undefined = "medium";

    const user = localStorage.getItem("user");
    if (user) {
        const user_json = JSON.parse(user);
        list_size = user_json.setting_list_size as "small" | "medium" | undefined;
    }

    return list_size;
}

export function getTheme() {
    const setting_theme = getSettingTheme();
    if (setting_theme == "dark") {
        return darkTheme;
    } else {
        return lightTheme;
    }
}

export async function saveSettingListProperties() {
    const list_settings: { key: string; value: string | null }[] = [];
    Object.keys(localStorage).forEach(function (ls_key) {
        if (ls_key.startsWith("RaStore.preferences")) {
            list_settings.push({ key: ls_key, value: localStorage.getItem(ls_key) });
        }
    });
    const list_setting_string = JSON.stringify(list_settings);
    saveSetting({ setting_list_properties: list_setting_string });
}

export function setListProperties(setting_list_properties: string) {
    if (setting_list_properties == null || setting_list_properties == "") {
        return;
    }
    const list_settings = JSON.parse(setting_list_properties);
    list_settings.forEach(function (ls: { key: string; value: string | null }) {
        if (ls.value != null) {
            localStorage.setItem(ls.key, ls.value);
        }
    });
}

function saveSetting(setting: any) {
    const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/my_settings/";

    httpClient(url, {
        method: "PATCH",
        body: JSON.stringify(setting),
    })
        .then((response) => {
            localStorage.setItem("user", JSON.stringify(response.json));
        })
        .catch((error) => {
            console.warn(error.message);
        });
}
