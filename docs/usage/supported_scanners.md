# Supported scanners

## Types

There are different types of vulnerability scans:

* **SCA / Software Composition Analysis**: Modern systems are not completely rewritten from scratch, but many basic functions are used as libraries. This applies not only to application code, but in the case of Docker, also to operating system functions and programmes. All these components can have known vulnerabilities that can be exploited by attackers.
* **Application SAST / Static Application Security Testing**: Many problems can be detected in the code through rule-based searches, e.g. injections or weak encryption. Tools exist for all common programming languages.
* **Infrastructure SAST**: Also for Infrastructure as Code (Dockerfile, Helm Charts, Terraform, ...) many problems can be found with rule-based searches before applying the code to set up the infrastructure.
* **Secrets**: Secrets such as passwords or API keys must not be checked into repositories with the code, and there are tools that search, for example, Git repositories across the entire version history for such secrets.
* **DAST / Dynamic Application Security Testing:**: This class is black-box security testing where the tests are performed by attacking an application (typically web applications or APIs) from the outside. The tests can be passive, where only anomalies are looked for, or active attacks on the system. 
* **Cloud infrastructure:** The running infrastructure, e.g. a Kubernetes cluster, can also be checked for vulnerabilities both with internal views (tests that run inside the infrastructure) and external views (tests from outside via the internet).
* **IAST / Interactive Application Security Testing**: IAST works inside an application by instrumenting the code to detect and report issues while the application is running.

## Data formats

While every vulnerability scanner writes its own format, there are 2 standardized formats that are implemented by several scanners:

* **[CycloneDX](https://cyclonedx.org/)**: CycloneDX is a Software Bill of Material (SBOM), that contains information about components of a system and their vulnerabilities. It is typically used by SCA scanners.
* **[SARIF](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=sarif)**: The Static Analysis Results Interchange Format is an OASIS standard which is implemented by a lot of SAST scanners.

This means the `CycloneDX` and `SARIF` parsers can import data from a variety of vulnerability scanners, while other vulnerability scanners need a dedicated parser for their special data format.

## Scanners

These scanners have been tested with SecObserve:

| Scanner | Parser | Type | Source |
|--------|---------|------|--------|
| [Dependency Check](https://jeremylong.github.io/DependencyCheck) | SARIF ^1)^ | SCA | API |
| [Dependency Track](https://dependencytrack.org) | Dependency Track | SCA | API |
| [Trivy Operator Prometheus](https://github.com/aquasecurity/trivy-operator) | JSON | Cloud infrastructure | API |
| [Grype](https://github.com/anchore/grype) | CycloneDX | SCA | File |
| [Trivy](https://aquasecurity.github.io/trivy) | CycloneDX | SCA | File |
| [Bandit](https://bandit.readthedocs.io/en/latest) | SARIF | Application SAST | File |
| [ESLint](https://github.com/nodesecurity/eslint-plugin-security) | SARIF | Application SAST | File |
| [Find-Sec-Bugs](https://find-sec-bugs.github.io) | SARIF | Application   SAST | File |
| [Semgrep](https://semgrep.dev/docs) | SARIF | Application SAST | File |
| [Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html) | SARIF | Infrastructure SAST | File |
| [KICS](https://docs.kics.io/latest) | SARIF | Infrastructure SAST | File |
| [tfsec](https://aquasecurity.github.io/tfsec) | SARIF | Infrastructure SAST | File |
| [Trivy](https://aquasecurity.github.io/trivy) | SARIF | Infrastructure SAST | File |
| [Trivy](https://aquasecurity.github.io/trivy) | SARIF | Secrets | File |
| [Gitleaks](https://gitleaks.io) | SARIF | Secrets | File |
| [CryptoLyzer](https://gitlab.com/coroner/cryptolyzer) ^2)^ | CryptoLyzer | DAST | File |
| [DrHeader](https://github.com/Santandersecurityresearch/DrHeader) | DrHeader | DAST | File |
| [ZAP](https://www.zaproxy.org) | ZAP | DAST | File |
| [Azure Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/) ^3)^ | Azure Defender | Cloud infrastructure | File |
| [Prowler 3](https://github.com/prowler-cloud/prowler)| Prowler 3 | Cloud infrastructure | File |
| [Prowler 4](https://github.com/prowler-cloud/prowler)| OCSF (Open Cybersecurity Schema Framework) | Cloud infrastructure | File |

^1)^ This is the exception to the rule. Even though SARIF is more suited for static code analysis, it works for Dependency Check.

^2)^ The CryptoLyzer parser checks the results (TLS versions, cipher suites, elliptic curves and signature algorithms) against BSI (Bundesamt für Sicherheit in der Informationssicherheit) recommendations.

 ^3)^ The results of Azure Defender for Cloud have to be exported manually in CSV format from the Azure Portal.

[GitHub actions and GitLab CI templates](../integrations/github_actions_and_templates.md) support running vulnerability checks and importing the results into SecObserve via GitHub workflows or GitLab CI pipelines in an efficient way.
