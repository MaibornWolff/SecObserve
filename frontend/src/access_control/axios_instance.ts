import axios, { InternalAxiosRequestConfig } from "axios";

import { get_oidc_id_token, jwt_signed_in, oidc_signed_in } from "./authProvider";

const axios_instance = axios.create({
    baseURL: window.__RUNTIME_CONFIG__.API_BASE_URL,
});

axios_instance.interceptors.request.use(
    async (config: InternalAxiosRequestConfig) => {
        if (oidc_signed_in()) {
            if (config.headers) {
                config.headers["Authorization"] = "Bearer " + get_oidc_id_token();
            }
            return config;
        } else if (jwt_signed_in()) {
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
