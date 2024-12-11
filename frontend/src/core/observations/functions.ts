export const IDENTIFIER_OBSERVATION_LIST = "observationlist";
export const IDENTIFIER_OBSERVATION_EMBEDDED_LIST = "observationembeddedlist";
export const IDENTIFIER_OBSERVATION_DASHBOARD_LIST = "observationdashboardlist";
export const IDENTIFIER_OBSERVATION_REVIEW_LIST = "observationreviewlist";
export const IDENTIFIER_OBSERVATION_REVIEW_LIST_PRODUCT = "observationreviewlistproduct";

export function setListIdentifier(identifier: string): void {
    localStorage.removeItem(IDENTIFIER_OBSERVATION_LIST);
    localStorage.removeItem(IDENTIFIER_OBSERVATION_EMBEDDED_LIST);
    localStorage.removeItem(IDENTIFIER_OBSERVATION_DASHBOARD_LIST);
    localStorage.removeItem(IDENTIFIER_OBSERVATION_REVIEW_LIST);
    localStorage.removeItem(IDENTIFIER_OBSERVATION_REVIEW_LIST_PRODUCT);

    localStorage.setItem(identifier, "true");
}
