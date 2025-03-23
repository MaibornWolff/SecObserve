import { User, WebStorageStateStore } from "oidc-client-ts";
import { UserManager } from "oidc-client-ts";

// eslint-disable-next-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-invalid-void-type
const onSigninCallback = (_user: User | void): void => {
    const user_manager = new UserManager(oidcConfig);
    user_manager.clearStaleState();
    const last_location = localStorage.getItem("last_location");
    if (last_location) {
        localStorage.removeItem("last_location");
        location.hash = last_location;
        window.location.replace("/" + last_location);
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

export const oidcStorageKey =
    "oidc.user:" + window.__RUNTIME_CONFIG__.OIDC_AUTHORITY + ":" + window.__RUNTIME_CONFIG__.OIDC_CLIENT_ID;

export function oidcStorageUser(): string | null {
    return localStorage.getItem(oidcStorageKey);
}

export function oidc_signed_in(): boolean {
    return oidcStorageUser() != null;
}

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

export const updateRefreshToken = () => {
    const oidcUser = oidcStorageUser();
    if (oidcUser) {
        const expires_at = JSON.parse(oidcUser).expires_at * 1000;
        if (expires_at < Date.now()) {
            localStorage.setItem("user_action", "refreshing token");
            const user_manager = new UserManager(oidcConfig);
            return user_manager
                .signinSilent()
                .then(() => {
                    return Promise.resolve();
                })
                .catch(() => {
                    return Promise.reject();
                });
        }
    }
    return Promise.resolve();
};
