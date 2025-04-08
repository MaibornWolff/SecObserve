import { httpClient } from "../commons/ra-data-django-rest-framework";
import {
    OBSERVATION_SEVERITY_CRITICAL,
    OBSERVATION_SEVERITY_HIGH,
    OBSERVATION_SEVERITY_LOW,
    OBSERVATION_SEVERITY_MEDIUM,
    OBSERVATION_SEVERITY_NONE,
    OBSERVATION_SEVERITY_UNKNOWN,
    OBSERVATION_STATUS_FALSE_POSITIVE,
    OBSERVATION_STATUS_NOT_AFFECTED,
    OBSERVATION_STATUS_NOT_SECURITY,
} from "../core/types";
import {
    EVALUATION_RESULT_ALLOWED,
    EVALUATION_RESULT_FORBIDDEN,
    EVALUATION_RESULT_IGNORED,
    EVALUATION_RESULT_REVIEW_REQUIRED,
    EVALUATION_RESULT_UNKNOWN,
} from "../licenses/types";
import { getSettingTheme } from "./user_settings/functions";

export function getIconAndFontColor() {
    if (getSettingTheme() == "dark") {
        return "white";
    } else {
        return "black";
    }
}

export function get_severity_color(severity: string): string {
    let backgroundColor = "transparent";
    switch (severity) {
        case OBSERVATION_SEVERITY_UNKNOWN:
            backgroundColor = "#00B4F0";
            break;
        case OBSERVATION_SEVERITY_NONE:
            backgroundColor = "#53aa33";
            break;
        case OBSERVATION_SEVERITY_LOW:
            backgroundColor = "#ffcb0d";
            break;
        case OBSERVATION_SEVERITY_MEDIUM:
            backgroundColor = "#f9a009";
            break;
        case OBSERVATION_SEVERITY_HIGH:
            backgroundColor = "#df3d03";
            break;
        case OBSERVATION_SEVERITY_CRITICAL:
            backgroundColor = "#cc0500";
            break;
    }
    return backgroundColor;
}

export function get_evaluation_result_color(record: any, evaluation_result: string | null): string {
    if (!evaluation_result) {
        if (record?.component_license_data) {
            evaluation_result = record.component_license_data.evaluation_result;
        } else {
            evaluation_result = record.evaluation_result;
        }
    }

    let backgroundColor = "transparent";
    switch (evaluation_result) {
        case EVALUATION_RESULT_ALLOWED:
            backgroundColor = "#53aa33";
            break;
        case EVALUATION_RESULT_FORBIDDEN:
            backgroundColor = "#df3d03";
            break;
        case EVALUATION_RESULT_REVIEW_REQUIRED:
            backgroundColor = "#f9a009";
            break;
        case EVALUATION_RESULT_UNKNOWN:
            backgroundColor = "#424242";
            break;
        case EVALUATION_RESULT_IGNORED:
            backgroundColor = "#424242";
            break;
    }
    return backgroundColor;
}

export function get_cwe_url(cwe: number): string {
    return "https://cwe.mitre.org/data/definitions/" + cwe + ".html";
}

export function get_cvss3_url(cvss_vector: string): string {
    if (cvss_vector.startsWith("CVSS:3.0/")) {
        return "https://www.first.org/cvss/calculator/3.0#" + cvss_vector;
    } else if (cvss_vector.startsWith("CVSS:3.1/")) {
        return "https://www.first.org/cvss/calculator/3.1#" + cvss_vector;
    }
    return "";
}

export function get_cvss4_url(cvss_vector: string): string {
    if (cvss_vector.startsWith("CVSS:4.0/")) {
        return "https://www.first.org/cvss/calculator/4.0#" + cvss_vector;
    }
    return "";
}

export function get_component_purl_url(
    component_name: string,
    component_version: string | null,
    component_purl_type: string | null,
    component_purl_namespace: string | null
): string | null {
    if (component_purl_type === null) {
        return null;
    }

    const typeArray: string[] = ["cargo", "golang", "maven", "npm", "nuget", "pypi"];
    if (!typeArray.includes(component_purl_type)) {
        return null;
    }

    let deps_dev_type = component_purl_type;
    if (component_purl_type === "golang") {
        deps_dev_type = "go";
    }

    let namespace_separator = "/";
    if (component_purl_type === "maven") {
        namespace_separator = ":";
    }

    let component_purl_url = "https://deps.dev/" + deps_dev_type + "/";
    if (component_purl_namespace !== null) {
        component_purl_url =
            component_purl_url + encodeURIComponent(component_purl_namespace) + encodeURIComponent(namespace_separator);
    }
    component_purl_url = component_purl_url + encodeURIComponent(component_name);
    if (component_version !== null) {
        component_purl_url = component_purl_url + "/" + component_version;
    }

    return component_purl_url;
}

const rtf = new Intl.RelativeTimeFormat("en", {
    localeMatcher: "best fit",
    numeric: "auto", // change to "always" if you want 1 day ago/from now
    // instead of yesterday/tomorrow
    style: "long",
});

export const humanReadableDate = (date: string | undefined) => {
    if (date === undefined) {
        return "";
    }

    const today = new Date().setHours(23, 59, 59, 999);
    const diffInMs = Date.parse(date).valueOf() - today.valueOf();
    const diffInDays = diffInMs / (1000 * 60 * 60 * 24);
    return rtf.format(Math.trunc(diffInDays), "day").replace(" ago", "");
};

export function set_settings_in_local_storage() {
    httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/status/settings/").then((response) => {
        localStorage.setItem("settings", JSON.stringify(response.json));
    });
}

export const feature_vex_enabled = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_vex");
        return feature_vex_position !== -1;
    } catch {
        return false;
    }
};

export function settings_risk_acceptance_expiry_date(): string | null {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const risk_acceptance_expiry_days = settings.risk_acceptance_expiry_days || null;
        if (risk_acceptance_expiry_days === null) {
            return null;
        }
        const date = new Date();
        date.setDate(date.getDate() + risk_acceptance_expiry_days);
        return date.toISOString().split("T")[0];
    } catch {
        return null;
    }
}

export const feature_general_rules_need_approval_enabled = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_general_rules_need_approval = features.indexOf("feature_general_rules_need_approval");
        return feature_general_rules_need_approval !== -1;
    } catch {
        return false;
    }
};

export const feature_license_management = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_license_management");
        return feature_vex_position !== -1;
    } catch {
        return false;
    }
};

export const feature_automatic_api_import = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_automatic_api_import");
        return feature_vex_position !== -1;
    } catch {
        return false;
    }
};

export const feature_automatic_osv_scanning = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_automatic_osv_scanning");
        return feature_vex_position !== -1;
    } catch {
        return false;
    }
};

export const feature_exploit_information = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_exploit_information");
        return feature_vex_position !== -1;
    } catch {
        return false;
    }
};

export const justificationIsEnabledForStatus = (status: string) => {
    const vex_enabled = feature_vex_enabled();
    const justification_recommended_for_status =
        [OBSERVATION_STATUS_NOT_AFFECTED, OBSERVATION_STATUS_NOT_SECURITY, OBSERVATION_STATUS_FALSE_POSITIVE].indexOf(
            status
        ) >= 0;
    return vex_enabled && justification_recommended_for_status;
};

export const is_superuser = () => {
    const user = localStorage.getItem("user");
    return user && JSON.parse(user).is_superuser;
};

export const is_external = () => {
    const user = localStorage.getItem("user");
    return user && JSON.parse(user).is_external;
};
