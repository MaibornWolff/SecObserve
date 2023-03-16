import { AuthProvider } from "react-admin";

import { getPublicClientApplication } from "../access_control/aad";
import { httpClient } from "../commons/ra-data-django-rest-framework";
import { getSettingTheme } from "../commons/settings/functions";

const authProvider: AuthProvider = {
    login: ({ username, password }) => {
        if (aad_signed_in()) {
            return Promise.resolve();
        } else {
            const request = new Request(
                window.__RUNTIME_CONFIG__.API_BASE_URL +
                    "/authentication/authenticate/",
                {
                    method: "POST",
                    body: JSON.stringify({ username, password }),
                    headers: new Headers({
                        "Content-Type": "application/json",
                    }),
                }
            );
            return fetch(request)
                .then((response) => {
                    if (response.status < 200 || response.status >= 300) {
                        throw new Error(response.statusText);
                    }
                    return response.json();
                })
                .then((auth) => {
                    localStorage.setItem("jwt", auth.jwt);
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
    logout: () => {
        localStorage.removeItem("jwt");
        localStorage.removeItem("user");
        localStorage.removeItem("aad_login_finalized");
        if (aad_signed_in()) {
            const pca = getPublicClientApplication();
            pca.logoutRedirect();
        }
        return Promise.resolve();
    },
    checkError: (error) => {
        if (error) {
            const status = error.status;
            if (status === 401 || status === 403) {
                localStorage.clear();
                return Promise.reject({
                    redirectTo: "/login",
                    logoutUser: false,
                });
            }
        }

        return Promise.resolve();
    },
    checkAuth: () => {
        if (localStorage.getItem("jwt") || aad_signed_in()) {
            return Promise.resolve();
        } else {
            if (localStorage.getItem("aad_login_finalized") == "false") {
                return Promise.resolve();
            } else {
                return Promise.reject();
            }
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
    return httpClient(
        window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/me/"
    ).then((response) => {
        const before_theme = getSettingTheme();
        localStorage.setItem("user", JSON.stringify(response.json));
        const after_theme = getSettingTheme();
        if (before_theme != after_theme) {
            window.location.reload();
        }
        return response.json;
    });
};

export function aad_signed_in(): boolean {
    const pca = getPublicClientApplication();
    return pca.getAllAccounts().length > 0;
}

export function jwt_signed_in(): boolean {
    return localStorage.getItem("jwt") != null;
}

export default authProvider;
