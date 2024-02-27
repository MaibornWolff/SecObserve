import { Identifier, RaRecord } from "react-admin";

export interface CSAF extends RaRecord {
    id: Identifier;
    user: Identifier;
    product: Identifier;
    vulnerablity_names: string;
    document_id_prefix: string;
    document_base_id: string;
    document_id: string;
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

export interface OpenVEX extends RaRecord {
    id: Identifier;
    user: Identifier;
    product: Identifier;
    vulnerablity_names: string;
    document_id_prefix: string;
    document_base_id: string;
    document_id: string;
    version: number;
    content_hash: string;
    author: string;
    role: string;
    timestamp: string;
    last_updated: string;
}
