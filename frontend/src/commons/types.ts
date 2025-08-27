export type ThemeName = "light" | "dark";

declare global {
    interface Window {
        restServer: any;
    }
}

export const VEX_JUSTIFICATION_TYPE_CSAF_OPENVEX = "CSAF/OpenVEX";
export const VEX_JUSTIFICATION_TYPE_CYCLONEDX = "CycloneDX";

export const VEX_JUSTIFICATION_TYPE_CHOICES = [
    { id: VEX_JUSTIFICATION_TYPE_CSAF_OPENVEX, name: VEX_JUSTIFICATION_TYPE_CSAF_OPENVEX },
    { id: VEX_JUSTIFICATION_TYPE_CYCLONEDX, name: VEX_JUSTIFICATION_TYPE_CYCLONEDX },
];
