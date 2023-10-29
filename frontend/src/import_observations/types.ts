import { Identifier, RaRecord } from "react-admin";

export interface ApiConfiguration extends RaRecord {
    id: Identifier;
    product: Identifier;
    name: string;
    parser: Identifier;
    base_url: string;
    project_key: string;
    api_key: string;
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
