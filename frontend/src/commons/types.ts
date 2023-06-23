import { Identifier, RaRecord } from "react-admin";

export type ThemeName = "light" | "dark";

declare global {
    interface Window {
        restServer: any;
    }
}
