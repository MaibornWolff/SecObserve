import { UserManager } from "oidc-client-ts";

import { oidcConfig, oidcStorageUser } from "./authProvider";

export const updateRefreshToken = () => {
    const oidcUser = oidcStorageUser();
    if (oidcUser) {
        const expires_at = JSON.parse(oidcUser).expires_at * 1000;
        if (expires_at < Date.now()) {
            localStorage.setItem("user_action", "refreshing token");
            const user_manager = new UserManager(oidcConfig);
            user_manager.signinSilent();
        }
    }
    return Promise.resolve();
};
