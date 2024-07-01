import { httpClient } from "../commons/ra-data-django-rest-framework";
import {
    OBSERVATION_SEVERITY_CRITICAL,
    OBSERVATION_SEVERITY_HIGH,
    OBSERVATION_SEVERITY_LOW,
    OBSERVATION_SEVERITY_MEDIUM,
    OBSERVATION_SEVERITY_NONE,
    OBSERVATION_SEVERITY_UNKOWN,
    OBSERVATION_STATUS_FALSE_POSITIVE,
    OBSERVATION_STATUS_NOT_AFFECTED,
    OBSERVATION_STATUS_NOT_SECURITY,
} from "../core/types";
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
        case OBSERVATION_SEVERITY_UNKOWN:
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
        default:
            null;
    }
    return backgroundColor;
}

export function get_cwe_url(cwe: number): string {
    return "https://cwe.mitre.org/data/definitions/" + cwe + ".html";
}

const VULNERABILITY_URLS = {
    CVE: "https://nvd.nist.gov/vuln/detail/",
    GHSA: "https://github.com/advisories/",
    OSV: "https://osv.dev/vulnerability/",
    PYSEC: "https://osv.dev/vulnerability/",
    SNYK: "https://snyk.io/vuln/",
    RUSTSEC: "https://rustsec.org/advisories/",
};

export function get_vulnerability_url(vulnerability_id: string): string | null {
    let return_value = null;

    Object.entries(VULNERABILITY_URLS).forEach((entry) => {
        const [key, value] = entry;
        if (vulnerability_id.startsWith(key)) {
            return_value = value + vulnerability_id;
        }
    });

    return return_value;
}

export function get_component_purl_url(
    component_name: string,
    component_version: string | null,
    purl_type: string | null,
    purl_namespace: string | null
): string | null {
    if (purl_type === null) {
        return null;
    }

    const typeArray: Array<string> = ["cargo", "go", "maven", "npm", "nuget", "pypi"];
    if (!typeArray.includes(purl_type)) {
        return null;
    }

    let component_purl_url = "https://deps.dev/" + purl_type + "/";
    if (!component_name.includes(":") && purl_namespace !== null) {
        component_purl_url = component_purl_url + purl_namespace + "%3A";
    }
    component_purl_url = component_purl_url + component_name;
    if (component_version !== null) {
        component_purl_url = component_purl_url + "/" + component_version;
    }

    return encodeURI(component_purl_url);
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

export async function set_settings_in_local_storage() {
    await httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/status/settings/").then((response) => {
        localStorage.setItem("settings", JSON.stringify(response.json));
    });
}

export const feature_vex_enabled = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_vex_position = features.indexOf("feature_vex");
        return feature_vex_position !== -1;
    } catch (e) {
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
        var date = new Date();
        date.setDate(date.getDate() + risk_acceptance_expiry_days);
        return date.toISOString().split("T")[0];
    } catch (e) {
        return null;
    }
}

export const feature_general_rules_need_approval_enabled = () => {
    try {
        const settings = JSON.parse(localStorage.getItem("settings") || "{}");
        const features = settings.features || [];
        const feature_general_rules_need_approval = features.indexOf("feature_general_rules_need_approval");
        return feature_general_rules_need_approval !== -1;
    } catch (e) {
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
