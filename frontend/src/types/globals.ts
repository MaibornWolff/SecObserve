export {};

declare global {
  interface Window {
    __RUNTIME_CONFIG__: {
      API_BASE_URL: string;
      AAD_ENABLE: string;
      AAD_AUTHORITY: string;
      AAD_CLIENT_ID: string;
      AAD_REDIRECT_URI: string;
      AAD_POST_LOGOUT_REDIRECT_URI: string;
      AAD_SCOPE: string;
    };
  }
}
