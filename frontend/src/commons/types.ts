import { Identifier, RaRecord } from "react-admin";

export type ThemeName = "light" | "dark";

export interface Notification extends RaRecord {
    id: Identifier;
    name: string;
    created: Date;
    message: string;
    user: Identifier;
    observation: Identifier;
    function: string;
    arguments: string;
}

declare global {
    interface Window {
        restServer: any;
    }
}
