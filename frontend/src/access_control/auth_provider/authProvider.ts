import { User, WebStorageStateStore } from "oidc-client-ts";
import { UserManager } from "oidc-client-ts";
import { AuthProvider } from "react-admin";

import { set_settings_in_local_storage } from "../../commons/functions";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { saveSettingListProperties, setListProperties } from "../../commons/user_settings/functions";

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
                    localStorage.setItem("theme", auth.user.setting_theme);
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
    checkError: async (error) => {
        if (error.status === 401) {
            if (oidc_signed_in()) {
                const user_manager = new UserManager(oidcConfig);
                localStorage.setItem("last_location", location.hash);
                await user_manager
                    .signinSilent()
                    .then(() => {
                        error.message = false;
                        error.logoutUser = false;
                        error.redirectTo = location.hash;
                        throw error;
                    })
                    .catch(() => {
                        localStorage.removeItem(oidcStorageKey);
                        return user_manager.signinRedirect();
                    });
            }
            throw error;
        }
    },
    checkAuth: () => {
        if (oidc_signed_in() || jwt_signed_in()) {
            return Promise.resolve();
        }
        return Promise.reject({ message: false });
    },
    getPermissions: () => Promise.reject(),
    getIdentity: async () => {
        const id = 0;
        let fullName = "";
        const avatar = undefined;

        let user = localStorage.getItem("user");
        if (!user) {
            await setUserInfo();
        }
        user = localStorage.getItem("user");
        if (user) {
            const user_json = JSON.parse(user);
            fullName = user_json.full_name;
        }

        set_settings_in_local_storage();

        return Promise.resolve({ id, fullName, avatar });
    },
};

export const setUserInfo = async () => {
    const userinfo = await getUserInfo();
    setListProperties(userinfo.setting_list_properties);
    delete userinfo.setting_list_properties;
    localStorage.setItem("user", JSON.stringify(userinfo));
    localStorage.setItem("theme", userinfo.setting_theme);
};

const getUserInfo = () => {
    return httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/users/me/").then((response) => {
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

// eslint-disable-next-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-invalid-void-type
const onSigninCallback = (_user: User | void): void => {
    const user_manager = new UserManager(oidcConfig);
    user_manager.clearStaleState();
    const last_location = localStorage.getItem("last_location");
    if (last_location) {
        localStorage.removeItem("last_location");
        location.hash = last_location;
        window.history.replaceState({}, document.title, "/" + last_location);
    } else {
        window.history.replaceState({}, document.title, window.location.pathname);
    }
};

export const oidcConfig = {
    userStore: new WebStorageStateStore({ store: window.localStorage }),
    authority: window.__RUNTIME_CONFIG__.OIDC_AUTHORITY,
    client_id: window.__RUNTIME_CONFIG__.OIDC_CLIENT_ID,
    redirect_uri: window.__RUNTIME_CONFIG__.OIDC_REDIRECT_URI,
    post_logout_redirect_uri: window.__RUNTIME_CONFIG__.OIDC_POST_LOGOUT_REDIRECT_URI,
    scope:
        window.__RUNTIME_CONFIG__.OIDC_SCOPE && window.__RUNTIME_CONFIG__.OIDC_SCOPE !== "dummy"
            ? window.__RUNTIME_CONFIG__.OIDC_SCOPE
            : "openid profile email",
    automaticSilentRenew: true,
    prompt: "select_account",
    onSigninCallback: onSigninCallback,
};

export function get_oidc_id_token(): string | null {
    if (oidcStorageUser()) {
        const user = User.fromStorageString(oidcStorageUser()!); // eslint-disable-line @typescript-eslint/no-non-null-assertion
        // We have checked before that user is not null
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
