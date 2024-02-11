import {
    OBSERVATION_SEVERITY_CRITICAL,
    OBSERVATION_SEVERITY_HIGH,
    OBSERVATION_SEVERITY_LOW,
    OBSERVATION_SEVERITY_MEDIUM,
    OBSERVATION_SEVERITY_NONE,
    OBSERVATION_SEVERITY_UNKOWN,
} from "../core/types";
import { getSettingTheme } from "./settings/functions";

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
    purl_type: string | null
): string | null {
    if (purl_type === null) {
        return null;
    }

    const typeArray: Array<string> = ["cargo", "go", "maven", "npm", "nuget", "pypi"];
    if (!typeArray.includes(purl_type)) {
        return null;
    }

    let component_purl_url = "https://deps.dev/" + purl_type + "/" + component_name;
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
