import { Identifier, RaRecord } from "react-admin";

export interface CSAF extends RaRecord {
    id: Identifier;
    user: Identifier;
    product: Identifier;
    vulnerablity_names: string;
    document_id_prefix: string;
    document_base_id: string;
    version: number;
    content_hash: string;
    title: string;
    tlp_label: string;
    tracking_initial_release_date: string;
    tracking_current_release_date: string;
    tracking_status: string;
    publisher_name: string;
    publisher_category: string;
    publisher_namespace: string;
}

export const CSAF_PUBLISHER_CATEGORY_CHOICES = [
    { id: "coordinator", name: "coordinator" },
    { id: "discoverer", name: "discoverer" },
    { id: "other", name: "other" },
    { id: "translator", name: "translator" },
    { id: "user", name: "user" },
    { id: "vendor", name: "vendor" },
];

export const CSAF_TLP_LABEL_CHOICES = [
    { id: "AMBER", name: "AMBER" },
    { id: "GREEN", name: "GREEN" },
    { id: "RED", name: "RED" },
    { id: "WHITE", name: "WHITE" },
];

export const CSAF_TRACKING_STATUS_CHOICES = [
    { id: "draft", name: "draft" },
    { id: "final", name: "final" },
    { id: "interim", name: "interim" },
];

export interface OpenVEX extends RaRecord {
    id: Identifier;
    user: Identifier;
    product: Identifier;
    vulnerablity_names: string;
    document_id_prefix: string;
    document_base_id: string;
    version: number;
    content_hash: string;
    author: string;
    role: string;
    timestamp: string;
    last_updated: string;
}

export interface CycloneDX extends RaRecord {
    id: Identifier;
    user: Identifier;
    product: Identifier;
    vulnerablity_names: string;
    document_id_prefix: string;
    version: number;
    content_hash: string;
    author: string;
    first_issued: string;
    last_updated: string;
}

export const VEX_STATUS_CHOICES = [
    { id: "not_affected", name: "not_affected" },
    { id: "affected", name: "affected" },
    { id: "fixed", name: "fixed" },
    { id: "under_investigation", name: "under_investigation" },
];
