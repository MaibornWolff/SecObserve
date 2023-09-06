import axios, { InternalAxiosRequestConfig } from "axios";

import { jwt_signed_in } from "./authProvider";

const axios_instance = axios.create({
    baseURL: window.__RUNTIME_CONFIG__.API_BASE_URL,
});

axios_instance.interceptors.request.use(
    async (config: InternalAxiosRequestConfig) => {
        // if (aad_signed_in()) {
        //     const publicClientApplication = getPublicClientApplication();
        //     const account = publicClientApplication.getAllAccounts()[0];
        //     const accessTokenRequest = {
        //         scopes: [window.__RUNTIME_CONFIG__.AAD_SCOPE as string],
        //         account: account,
        //     };
        //     if (account) {
        //         const accessTokenResponse = await publicClientApplication.acquireTokenSilent(accessTokenRequest);

        //         if (accessTokenResponse) {
        //             const accessToken = accessTokenResponse.accessToken;

        //             if (config.headers && accessToken) {
        //                 config.headers["Authorization"] = "Bearer " + accessToken;
        //             }
        //         }
        //     }
        //     return config;
        // } else if (jwt_signed_in()) {
        // } else if (jwt_signed_in()) {
        if (jwt_signed_in()) {
            if (config.headers) {
                config.headers["Authorization"] = "JWT " + localStorage.getItem("jwt");
            }
            return config;
        } else {
            return config;
        }
    },
    (error) => {
        Promise.reject(error);
    }
);

export default axios_instance;
