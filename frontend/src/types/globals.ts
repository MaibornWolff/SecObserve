export {};

declare global {
    interface Window {
        __RUNTIME_CONFIG__: {
            API_BASE_URL: string;
            OAUTH2_ENABLE: string;
            OAUTH2_AUTHORITY: string;
            OAUTH2_CLIENT_ID: string;
            OAUTH2_REDIRECT_URI: string;
            OAUTH2_POST_LOGOUT_REDIRECT_URI: string;
            OAUTH2_SCOPE: string;
        };
    }
}
