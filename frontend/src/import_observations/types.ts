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
