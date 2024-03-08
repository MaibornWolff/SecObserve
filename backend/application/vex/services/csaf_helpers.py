VULNERABILITY_ECOSYSTEM = {
    "GHSA": "GitHub Security Advisory",
    "OSV": "Open Source Vulnerability Database",
    "PYSEC": "Python Packaging Advisory Database",
    "SNYK": "Snyk",
    "RUSTSEC": "Rust Security Advisory Database",
}


# create url for vulnerability
def get_vulnerability_ecosystem(vulnerability_name: str) -> str:
    for key, value in VULNERABILITY_ECOSYSTEM.items():
        if vulnerability_name.startswith(key):
            return value
    return "Unkonwn ecosystem"
