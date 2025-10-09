import axios, { InternalAxiosRequestConfig } from "axios";

import { jwt_signed_in } from "../../access_control/auth_provider/authProvider";
import { get_oidc_id_token, oidc_signed_in } from "../../access_control/auth_provider/oidc";

const axios_instance = axios.create({
    baseURL: window.__RUNTIME_CONFIG__.API_BASE_URL,
});

axios_instance.interceptors.request.use(
    async (config: InternalAxiosRequestConfig) => {
        if (oidc_signed_in()) {
            if (config.headers) {
                config.headers.Authorization = "Bearer " + get_oidc_id_token();
            }
            return config;
        } else if (jwt_signed_in()) {
            if (config.headers) {
                config.headers.Authorization = "JWT " + localStorage.getItem("jwt");
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
