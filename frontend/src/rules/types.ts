import { Identifier, RaRecord } from "react-admin";

export interface GeneralRule extends RaRecord {
    id: Identifier;
    name: string;
    description: string;
    parser: Identifier;
    scanner_prefix: string;
    title: string;
    description_observation: string;
    origin_component_name_version: string;
    origin_docker_image_name_tag: string;
    origin_endpoint_url: string;
    origin_service_name: string;
    origin_source_file: string;
    new_severity: string;
    new_status: string;
}

export interface ProductRule extends RaRecord {
    id: Identifier;
    name: string;
    description: string;
    product: Identifier;
    parser: Identifier;
    scanner_prefix: string;
    title: string;
    origin_component_name_version: string;
    origin_docker_image_name_tag: string;
    origin_endpoint_url: string;
    origin_service_name: string;
    origin_source_file: string;
    new_severity: string;
    new_status: string;
    enabled: boolean;
}
