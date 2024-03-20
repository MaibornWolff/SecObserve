![SecObserve](frontend/public/secobserve.svg)

# SecObserve

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8388/badge)](https://www.bestpractices.dev/projects/8388) [![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/MaibornWolff/SecObserve/badge)](https://securityscorecards.dev/viewer/?uri=github.com/MaibornWolff/SecObserve)


SecObserve is an open source vulnerability management system for software development and cloud environments. It supports a variety of open source vulnerability scanners and integrates easily into CI/CD pipelines. Results about potential security flaws from various vulnerability scanning tools are made available for assessment and reporting.

![Dashboard](docs/assets/images/screenshot_dashboard.png)

## Overview

The aim of SecObserve is to make vulnerability scanning and vulnerability management as easy as possible for software development projects using open source tools. It consists of 2 major components:

* **Vulnerability management system SecObserve:** SecObserve provides the development team with an overview of the results of all vulnerability scans for their project, which can be easily filtered and sorted. In the detailed view, the results are displayed uniformly with a wealth of information, regardless of which vulnerability scanner generated them.

    With the help of automatically executed rules and manual assessments, the results can be efficiently evaluated to eliminate irrelevant results and accept risks. This allows the development team to concentrate on fixing the relevant vulnerabilities.

* **GitLab CI templates and GitHub actions:** Integrating vulnerability scanners into a CI/CD pipeline can be tedious. Each tool has to be installed differently and is called with different parameters. To avoid having to solve this task all over again, there are repositories with GitLab CI Templates and GitHub Actions. These make the process of integrating vulnerability scanners very simple by providing uniform methods for launching the tools and uniform parameters. The tools are regularly updated in the repositories so that the latest features and bug fixes are always available.

    All templates run the scanner, upload the results into SecObserve and make the results of the scans available for download as artefacts in JSON format.

    The sources of the GitHub actions and GitLab CI templates can be found in [https://github.com/MaibornWolff/secobserve_actions_templates](https://github.com/MaibornWolff/secobserve_actions_templates).

![Overview](docs/assets/images/secobserve_process.svg)

## Integrations

![Overview](docs/assets/images/secobserve_integrations.svg)

## Documentation

The full documentation how to install and use Secobserve can be found here: [https://maibornwolff.github.io/SecObserve/](https://maibornwolff.github.io/SecObserve/)

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Contributing

Please see the [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get involved in the project.

## License

SecObserve is licensed under the [3-Clause BSD License](LICENSE.txt)
