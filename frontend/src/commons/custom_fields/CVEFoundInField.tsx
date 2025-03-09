import { Stack } from "@mui/material";
import { ReactNode } from "react";

import TextUrlField from "./TextUrlField";

interface CVEFoundInFieldProps {
    cve_found_in: any;
    vulnerability_id: string;
}

const Divider: ReactNode = <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>;

const CVEFoundInField = ({ cve_found_in, vulnerability_id }: CVEFoundInFieldProps) => {
    let cisa_url = null;
    let exploit_db_url = null;
    let metasploit_url = null;
    let nuclei_url = null;
    let vulncheck_url = null;
    let poc_github_url = null;
    for (const item of cve_found_in) {
        switch (item.source) {
            case "CISA KEV": {
                cisa_url =
                    "https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=" +
                    vulnerability_id;
                break;
            }
            case "Exploit-DB": {
                exploit_db_url = "https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv";
                break;
            }
            case "Metasploit": {
                metasploit_url =
                    "https://raw.githubusercontent.com/rapid7/metasploit-framework/master/db/modules_metadata_base.json";
                break;
            }
            case "Nuclei": {
                nuclei_url = "https://raw.githubusercontent.com/projectdiscovery/nuclei-templates/main/cves.json";
                break;
            }
            case "PoC GitHub": {
                const cve_parts = vulnerability_id.split("-");
                if (cve_parts.length === 3) {
                    const year = cve_parts[1];
                    poc_github_url =
                        "https://github.com/nomi-sec/PoC-in-GitHub/tree/master/" +
                        year +
                        "/" +
                        vulnerability_id +
                        ".json";
                }
                break;
            }
            case "VulnCheck KEV": {
                vulncheck_url = "https://vulncheck.com/cve/" + vulnerability_id;
                break;
            }
        }
    }
    return (
        <Stack direction="row" spacing={0}>
            {cisa_url && <TextUrlField text="CISA KEV" url={cisa_url} label="Source" new_tab={true} />}
            {cisa_url && (exploit_db_url || metasploit_url || nuclei_url || poc_github_url || vulncheck_url) && Divider}
            {exploit_db_url && <TextUrlField text="Exploit-DB" url={exploit_db_url} label="Source" new_tab={true} />}
            {exploit_db_url && (metasploit_url || nuclei_url || poc_github_url || vulncheck_url) && Divider}
            {metasploit_url && <TextUrlField text="Metasploit" url={metasploit_url} label="Source" new_tab={true} />}
            {metasploit_url && (nuclei_url || poc_github_url || vulncheck_url) && Divider}
            {nuclei_url && <TextUrlField text="Nuclei" url={nuclei_url} label="Source" new_tab={true} />}
            {nuclei_url && (poc_github_url || vulncheck_url) && Divider}
            {poc_github_url && <TextUrlField text="PoC GitHub" url={poc_github_url} label="Source" new_tab={true} />}
            {poc_github_url && vulncheck_url && Divider}
            {vulncheck_url && <TextUrlField text="VulnCheck KEV" url={vulncheck_url} label="Source" new_tab={true} />}
        </Stack>
    );
};

export default CVEFoundInField;
