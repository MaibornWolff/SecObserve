/**
 * Copyright (c) 2020 Bojan Mihelac under the MIT License
 * See https://github.com/bmihelac/ra-data-django-rest-framework
 * Copied to make it compatible with React-Admin 4 and DefectDojo
 */
import { InteractionRequiredAuthError } from "@azure/msal-browser";
import queryString from "query-string";
import { DataProvider, Identifier, fetchUtils } from "react-admin";

import { getPublicClientApplication } from "../../access_control/aad";
import { aad_signed_in, jwt_signed_in } from "../../access_control/authProvider";

const base_url = window.__RUNTIME_CONFIG__.API_BASE_URL;

const getPaginationQuery = (params: any) => {
    return {
        page: params.pagination.page,
        page_size: params.pagination.perPage,
    };
};

const getFilterQuery = (params: any) => {
    const { q: search, ...otherSearchParams } = params.filter;
    return {
        ...otherSearchParams,
        search,
    };
};

export const getOrderingQuery = (params: any) => {
    const { field, order } = params.sort;
    return {
        ordering: `${order === "ASC" ? "" : "-"}${field}`,
    };
};

function createOptionsFromTokenJWT() {
    return {
        user: {
            authenticated: true,
            token: "JWT " + localStorage.getItem("jwt"),
        },
    };
}

export async function httpClient(url: string, options?: fetchUtils.Options | undefined) {
    if (aad_signed_in()) {
        const publicClientApplication = getPublicClientApplication();
        await publicClientApplication.initialize();
        const account = publicClientApplication.getAllAccounts()[0];
        const accessTokenRequest = {
            scopes: [window.__RUNTIME_CONFIG__.AAD_SCOPE as string],
            account: account,   
        };
        const authResult = await publicClientApplication.acquireTokenSilent(accessTokenRequest).catch((error) => {
            console.warn("silent token acquisition fails. acquiring token using redirect");
            if (error instanceof InteractionRequiredAuthError) {
                // fallback to interaction when silent call fails
                return publicClientApplication
                    .acquireTokenRedirect(accessTokenRequest)
                    .then((tokenResponse) => {
                        return tokenResponse;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            } else {
                console.warn(error);
            }
        });
        const token = authResult?.accessToken;
        const user = {
            authenticated: !!token,
            token: `Bearer ${token}`,
        };
        return fetchUtils.fetchJson(url, { ...options, user });
    } else if (jwt_signed_in()) {
        return fetchUtils.fetchJson(url, Object.assign(createOptionsFromTokenJWT(), options));
    } else {
        return Promise.reject();
    }
}

export default (): DataProvider => {
    const getOneJson = (resource: string, id: Identifier) => {
        return httpClient(`${base_url}/${resource}/${id}/`).then((response) => {
            return response.json;
        });
    };

    return {
        getList: async (resource, params) => {
            const query = {
                ...getFilterQuery(params),
                ...getPaginationQuery(params),
                ...getOrderingQuery(params),
            };

            const url = `${base_url}/${resource}/?${queryString.stringify(query)}`;

            const { json } = await httpClient(url);

            return {
                data: json.results,
                total: json.count,
            };
        },

        getOne: async (resource, params) => {
            const data = await getOneJson(resource, params.id);
            return {
                data,
            };
        },

        getMany: (resource, params) => {
            return Promise.all(params.ids.map((id) => getOneJson(resource, id))).then((data) => ({ data }));
        },

        getManyReference: async (resource, params) => {
            const query = {
                ...getFilterQuery(params),
                ...getPaginationQuery(params),
                ...getOrderingQuery(params),
                [params.target]: params.id,
            };
            const url = `${base_url}/${resource}/?${queryString.stringify(query)}`;

            const { json } = await httpClient(url);
            return {
                data: json.results,
                total: json.count,
            };
        },

        update: async (resource, params) => {
            const { json } = await httpClient(`${base_url}/${resource}/${params.id}/`, {
                method: "PATCH",
                body: JSON.stringify(params.data),
            });
            return { data: json };
        },

        updateMany: (resource, params) =>
            Promise.all(
                params.ids.map((id) =>
                    httpClient(`${base_url}/${resource}/${id}/`, {
                        method: "PATCH",
                        body: JSON.stringify(params.data),
                    })
                )
            ).then((responses) => ({
                data: responses.map(({ json }) => json.id),
            })),

        create: async (resource, params) => {
            const { json } = await httpClient(`${base_url}/${resource}/`, {
                method: "POST",
                body: JSON.stringify(params.data),
            });
            return {
                data: { ...json },
            };
        },

        delete: async (resource, params) => {
            const { json } = await httpClient(`${base_url}/${resource}/${params.id}/`, {
                method: "DELETE",
            });
            return { data: json };
        },

        deleteMany: (resource, params) =>
            Promise.all(
                params.ids.map((id) =>
                    httpClient(`${base_url}/${resource}/${id}/`, {
                        method: "DELETE",
                    })
                )
            ).then(() => ({ data: [] })),
    };
};
