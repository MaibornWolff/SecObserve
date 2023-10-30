import { User, WebStorageStateStore } from "oidc-client-ts";
import { UserManager } from "oidc-client-ts";
import { AuthProvider } from "react-admin";

import { httpClient } from "../commons/ra-data-django-rest-framework";
import { getSettingTheme, saveSettingListProperties, setListProperties } from "../commons/settings/functions";

const authProvider: AuthProvider = {
    login: ({ username, password }) => {
        if (oidc_signed_in()) {
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
        if (oidc_signed_in() || jwt_signed_in()) {
            await saveSettingListProperties();
        }

        localStorage.removeItem("jwt");
        localStorage.removeItem("user");

        if (oidc_signed_in()) {
            const user_manager = new UserManager(oidcConfig);
            return user_manager.signoutRedirect();
        }

        return Promise.resolve();
    },
    checkError: (error) => {
        if (error) {
            const status = error.status;
            if (status === 401 || status === 403) {
                return Promise.reject({ message: error.message });
            }
        }
        return Promise.resolve();
    },
    checkAuth: () => {
        if (oidc_signed_in() || jwt_signed_in()) {
            return Promise.resolve();
        } else {
            return Promise.reject({ message: false });
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

export const oidcStorageKey =
    "oidc.user:" + window.__RUNTIME_CONFIG__.OIDC_AUTHORITY + ":" + window.__RUNTIME_CONFIG__.OIDC_CLIENT_ID;

export function oidcStorageUser(): string | null {
    return localStorage.getItem(oidcStorageKey);
}

export function oidc_signed_in(): boolean {
    return oidcStorageUser() != null;
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const onSigninCallback = (_user: User | void): void => {
    window.history.replaceState({}, document.title, window.location.pathname);
};

export const oidcConfig = {
    userStore: new WebStorageStateStore({ store: window.localStorage }),
    authority: window.__RUNTIME_CONFIG__.OIDC_AUTHORITY,
    client_id: window.__RUNTIME_CONFIG__.OIDC_CLIENT_ID,
    redirect_uri: window.__RUNTIME_CONFIG__.OIDC_REDIRECT_URI,
    post_logout_redirect_uri: window.__RUNTIME_CONFIG__.OIDC_POST_LOGOUT_REDIRECT_URI,
    scope: "openid profile email",
    automaticSilentRenew: true,
    prompt: "select_account",
    onSigninCallback: onSigninCallback,
};

export function get_oidc_id_token(): string | null {
    if (oidcStorageUser()) {
        const user = User.fromStorageString(oidcStorageUser()!);
        if (user && user.id_token) {
            return user.id_token;
        } else {
            return null;
        }
    } else {
        return null;
    }
}

export default authProvider;
