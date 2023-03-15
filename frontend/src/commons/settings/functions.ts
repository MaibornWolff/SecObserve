import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { darkTheme, lightTheme } from "../layout/themes";

export function setSettingTheme(theme: string) {
    const patch = {
        setting_theme: theme,
    };

    const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/my_settings/";

    httpClient(url, {
        method: "PATCH",
        body: JSON.stringify(patch),
    })
        .then((response) => {
            localStorage.setItem("user", JSON.stringify(response.json));
        })
        .catch((error) => {
            console.warn(error.message);
        });
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

export function getTheme() {
    const setting_theme = getSettingTheme();
    if (setting_theme == "dark") {
        return darkTheme;
    } else {
        return lightTheme;
    }
}
