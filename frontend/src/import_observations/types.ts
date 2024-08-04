import { Identifier, RaRecord } from "react-admin";

export interface ApiConfiguration extends RaRecord {
    id: Identifier;
    product: Identifier;
    name: string;
    parser: Identifier;
    base_url: string;
    project_key: string;
    api_key: string;
    query: string;
}

export interface VulnerabilityCheck extends RaRecord {
    id: Identifier;
    product: Identifier;
    branch: Identifier;
    branch_name: string;
    scanner: string;
    scanner_name: string;
    filename: string;
    api_configuration_name: string;
    first_import: Date;
    last_import: string;
    last_import_observations_new: number;
    last_import_observations_updated: number;
    last_import_observations_resolved: number;
}
export interface Parser extends RaRecord {
    id: Identifier;
    name: string;
    type: string;
    source: string;
}

export const SCANNER_TYPE_CHOICES = [
    { id: "SCA", name: "SCA" },
    { id: "SAST", name: "SAST" },
    { id: "DAST", name: "DAST" },
    { id: "IAST", name: "IAST" },
    { id: "Secrets", name: "Secrets" },
    { id: "Infrastructure", name: "Infrastructure" },
    { id: "Other", name: "Other" },
    { id: "Manual", name: "Manual" },
];

export const PARSER_SOURCE_CHOICES = [
    { id: "API", name: "API" },
    { id: "File", name: "File" },
    { id: "Manual", name: "Manual" },
    { id: "Unkown", name: "Unkown" },
];
