import { PublicClientApplication } from "@azure/msal-browser";

// Msal Configurations
const config = {
    auth: {
        authority: window.__RUNTIME_CONFIG__.AAD_AUTHORITY,
        clientId: window.__RUNTIME_CONFIG__.AAD_CLIENT_ID as string,
        redirectUri: window.__RUNTIME_CONFIG__.AAD_REDIRECT_URI,
        postLogoutRedirectUri:
            window.__RUNTIME_CONFIG__.AAD_POST_LOGOUT_REDIRECT_URI,
        navigateToLoginRequestUrl: true,
    },
    cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false,
    },
};

// Add scopes here for ID token to be used at Microsoft identity platform endpoints.
export const loginRequest = {
    scopes: ["User.Read"],
};

export function getPublicClientApplication() {
    return new PublicClientApplication(config);
}
