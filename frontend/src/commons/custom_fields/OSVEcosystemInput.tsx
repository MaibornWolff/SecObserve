import { Fragment } from "react";
import { TextInput } from "react-admin";

import { AutocompleteInputMedium } from "../layout/themes";
import TextUrlField from "./TextUrlField";

const ECOSYSTEMS_CHOICES = [
    { id: "AlmaLinux", name: "AlmaLinux" },
    { id: "Alpine", name: "Alpine" },
    { id: "Debian", name: "Debian" },
    { id: "Mageia", name: "Mageia" },
    { id: "openSUSE", name: "openSUSE" },
    { id: "Photon OS", name: "Photon OS" },
    { id: "Red Hat", name: "Red Hat" },
    { id: "Rocky Linux", name: "Rocky Linux" },
    { id: "SUSE", name: "SUSE" },
    { id: "Ubuntu", name: "Ubuntu" },
];

const OSVEcosystemInput = () => {
    return (
        <Fragment>
            <AutocompleteInputMedium
                source="osv_linux_ecosystem"
                label="OSV Linux ecosystem"
                choices={ECOSYSTEMS_CHOICES}
            />
            <TextInput source="osv_linux_release" label="OSV Linux release" />
            <TextUrlField
                url="https://ossf.github.io/osv-schema/#affectedpackage-field"
                text="OSV affected package specification"
            />
        </Fragment>
    );
};

export default OSVEcosystemInput;
