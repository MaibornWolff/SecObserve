import { AuthProvider } from "react-admin";

import { httpClient } from "../commons/ra-data-django-rest-framework";
import { getSettingTheme, saveSettingListProperties, setListProperties } from "../commons/settings/functions";

const authProvider: AuthProvider = {
    login: ({ username, password }) => {
        if (oauth2_signed_in()) {
            return Promise.resolve();
        } else {
            const request = new Request(window.__RUNTIME_CONFIG__.API_BASE_URL + "/authentication/authenticate/", {
                method: "POST",
                body: JSON.stringify({ username, password }),
                headers: new Headers({
                    "Content-Type": "application/json",
                }),
            });
            return fetch(request)
                .then((response) => {
                    if (response.status < 200 || response.status >= 300) {
                        throw new Error(response.statusText);
                    }
                    return response.json();
                })
                .then((auth) => {
                    localStorage.setItem("jwt", auth.jwt);
                    setListProperties(auth.user.setting_list_properties);
                    delete auth.user.setting_list_properties;
                    localStorage.setItem("user", JSON.stringify(auth.user));
                })
                .catch((error) => {
                    if (error.message == "Forbidden") {
                        throw new Error("Invalid credentials");
                    } else {
                        throw new Error("Network error");
                    }
                });
        }
    },
    logout: async () => {
        if (oauth2_signed_in() || jwt_signed_in()) {
            await saveSettingListProperties();
        }

        localStorage.removeItem("jwt");
        localStorage.removeItem("user");
        if (oauth2_signed_in()) {
            // ToDo
        }

        return Promise.resolve();
    },
    checkError: (error) => {
        if (error) {
            const status = error.status;
            if (status === 401 || status === 403) {
                Object.keys(localStorage).forEach(function (key) {
                    if (!key.startsWith("RaStore")) {
                        localStorage.removeItem(key);
                    }
                });
                return Promise.reject({
                    redirectTo: "/login",
                    logoutUser: false,
                });
            }
        }

        return Promise.resolve();
    },
    checkAuth: () => {
        if (localStorage.getItem("jwt") || oauth2_signed_in()) {
            return Promise.resolve();
        } else {
            return Promise.reject();
        }
    },
    getPermissions: () => Promise.reject(),
    getIdentity: async () => {
        const id = 0;
        let fullName = "";
        const avatar = undefined;

        const user = localStorage.getItem("user");
        if (user) {
            const user_json = JSON.parse(user);
            fullName = user_json.full_name;
        } else {
            const userinfo = await getUserInfo();
            const { id: id, full_name: fullName, username: avatar } = userinfo;
            return Promise.resolve({ id, fullName, avatar });
        }

        return Promise.resolve({ id, fullName, avatar });
    },
};

const getUserInfo = async () => {
    return httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/me/").then((response) => {
        const before_theme = getSettingTheme();
        setListProperties(response.json.setting_list_properties);
        delete response.json.setting_list_properties;
        localStorage.setItem("user", JSON.stringify(response.json));
        const after_theme = getSettingTheme();
        if (before_theme != after_theme) {
            window.location.reload();
        }
        return response.json;
    });
};

export function jwt_signed_in(): boolean {
    return localStorage.getItem("jwt") != null;
}

export function oauth2_signed_in(): boolean {
    const oidcStorage = localStorage.getItem(
        "oidc.user:https://login.microsoftonline.com/b8d7ad48-53f4-4c29-a71c-0717f0d3a5d0:46e202b4-dd0f-4bf3-897c-cfdf6b1547a9"
    );
    console.log("--- oidcStorage --- " + oidcStorage + "---");
    return oidcStorage != null;
}

export default authProvider;
