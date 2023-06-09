# GitHub actions and GitLab CI templates

Integrating vulnerability scanners in a CI/CD pipeline can be cumbersome. Every tool is different to install and has different parameters. Our repository of GitHub actions and GitLab CI templates makes this process very straightforward, with a unified way to start the tools. The tools in the template repository will be updated regularly, so that all the latest features and bugfixes are available.

All actions and templates run the scanner, import the results into SecObserve and make the report available as an artifact.

 The actions and the templates are stored in the repository [https://github.com/MaibornWolff/secobserve_actions_templates](https://github.com/MaibornWolff/secobserve_actions_templates).

## Variables

Most of the actions and templates use the same set of variables:

| Variable | Optionality | Description |
|----------|-------------|-------------|
| **Scanning** |
| `TARGET` | *mandatory* | The target to be scanned, often it is a path of the filesystem, but can be a Docker image, an URL or others. |
| `REPORT_NAME` | *mandatory* | The name of the report to be written. It will be saved as an artifact. |
| `RUN_DIRECTORY` | *optional* | The directory where to run the scanner, only to be used when the `TARGET` is a path. |
| `FURTHER_PARAMETERS` | *optional* | Further parameters to be given to the scanner. |
| `CONFIGURATION` | *mandatory, only for Semgrep* | Configuration to be used with Semgrep. |
| `RULES` | *optional, only for DrHeader* | Custom rules to be used with DrHeader. |
| `SCRIPT` | *optional, only for OWASP ZAP* | Script to be executed, default is `zap-baseline.py`. |
| **Importing** |
| `SO_UPLOAD` | *optional* | No upload of observations into SecObserve if value is not `true`, default is `true`. |
| `SO_API_BASE_URL` | *mandatory* | Base URL of the SecObserve backend, e.g. `https://secobserve-backend.example.com`. |
| `SO_API_TOKEN` | *mandatory* | API token of the user to be used for the import. The users needs at least the `Upload` role. |
| `SO_PRODUCT_NAME` | *mandatory* | Name of the product which observations are imported. The product has to exist before starting the import. |
| `SO_BRANCH_NAME` | *optional* | Name of the branch in the source code repository. |
| `SO_ORIGIN_SERVICE` | *optional* | Service name to be set for all imported observations. |
| `SO_ORIGIN_DOCKER_IMAGE_NAME_TAG` | *optional* | Name:Tag of Docker image to be set for all imported observations. |
| `SO_ORIGIN_ENDPOINT_URL` | *optional* | URL of endpoint to be set for all imported observations. |

## Available actions and templates

| Scanner | GitHub Action | GitLab CI Template | License |
|----------|---------|-------------|--------|
| [Bandit](https://bandit.readthedocs.io/en/latest)                 | `actions/SAST/bandit` | `templates/SAST/bandit.yml` | [Apache 2.0](https://github.com/PyCQA/bandit/blob/main/LICENSE) |
| [ESLint](https://github.com/eslint/eslint)                        | `actions/SAST/eslint` | `templates/SAST/eslint.yml` | [MIT](https://github.com/eslint/eslint/blob/main/LICENSE) |
| [Semgrep](https://semgrep.dev/docs)                               | `actions/SAST/semgrep` | `templates/SAST/semgrep.yml` |[LGPL 2.1](https://github.com/returntocorp/semgrep/blob/develop/LICENSE) |
| [Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html)    | `actions/SAST/checkov` | `templates/SAST/checkov.yml` | [Apache 2.0](https://github.com/bridgecrewio/checkov/blob/main/LICENSE) |
| [KICS](https://docs.kics.io/latest)                               | `actions/SAST/kics` | `templates/SAST/kics.yml` | [Apache 2.0](https://github.com/Checkmarx/kics/blob/master/LICENSE) |
| [Grype](https://github.com/anchore/grype)                         | `actions/SCA/grype_image` | `templates/SCA/grype_image.yml` | [Apache 2.0](https://github.com/anchore/grype/blob/main/LICENSE) |
| [Trivy](https://aquasecurity.github.io/trivy)                     | `actions/SCA/trivy_filesystem` | `templates/SCA/trivy_filesystem.yml` | [Apache 2.0](https://github.com/aquasecurity/trivy/blob/main/LICENSE) |
| [Trivy](https://aquasecurity.github.io/trivy)                     | `actions/SCA/trivy_image` | `templates/SCA/trivy_image.yml` | [Apache 2.0](https://github.com/aquasecurity/trivy/blob/main/LICENSE) |
| [Gitleaks](https://gitleaks.io)                                   | `actions/secrets/gitleaks` | `templates/secrets/gitleaks.yml` | [MIT](https://github.com/gitleaks/gitleaks/blob/master/LICENSE) |
| [CryptoLyzer](https://gitlab.com/coroner/cryptolyzer)             | `actions/DAST/cryptolyzer` | `templates/DAST/cryptolyzer.yml` | [MPL 2.0](https://gitlab.com/coroner/cryptolyzer/-/blob/master/LICENSE.txt) |
| [DrHeader](https://github.com/Santandersecurityresearch/DrHeader) | `actions/DAST/drheader` | `templates/DAST/drheader.yml` | [MIT](https://github.com/Santandersecurityresearch/DrHeader/blob/master/LICENSE) |
| [OWASP ZAP](https://github.com/zaproxy/zaproxy)                   | `actions/DAST/owasp_zap` | `templates/DAST/owasp_zap.yml` | [Apache 2.0](https://github.com/zaproxy/zaproxy/blob/main/LICENSE) |

All GitHub actions and GitLab CI templates use a pre-built Docker image that contains all scanners and the SecObserve importer.

##  Examplary workflow for GitHub actions

!!! tip
    The mandatory variables for importing (`SO_API_BASE_URL`, `SO_API_TOKEN`, `SO_PRODUCT_NAME`) can be set as secrets and variables in the settings of the project in GitHub.

```yaml
name: Vulnerability checks

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Bandit
        uses: MaibornWolff/secobserve_actions_templates/actions/SAST/bandit@main
        with:
          target: 'dd_import'
          report_name: 'dd_import_bandit.sarif'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run Semgrep
        uses: MaibornWolff/secobserve_actions_templates/actions/SAST/semgrep@main
        with:
          target: 'dd_import'
          report_name: 'dd_import_semgrep.json'
          configuration: 'r/python'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run KICS
        uses: MaibornWolff/secobserve_actions_templates/actions/SAST/kics@main
        with:
          target: '.'
          report_name: 'dd_import_kics.sarif'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run Checkov
        uses: MaibornWolff/secobserve_actions_templates/actions/SAST/checkov@main
        with:
          target: '.'
          report_name: 'dd_import_checkov.sarif'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run Trivy image
        uses: MaibornWolff/secobserve_actions_templates/actions/SCA/trivy_image@main
        with:
          target: 'maibornwolff/dd-import:latest'
          report_name: 'dd_import_trivy_image.json'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run Grype image
        uses: MaibornWolff/secobserve_actions_templates/actions/SCA/grype_image@main
        with:
          target: 'maibornwolff/dd-import:latest'
          report_name: 'dd_import_grype_image.json'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Run Gitleaks
        uses: MaibornWolff/secobserve_actions_templates/actions/secrets/gitleaks@main
        with:
          report_name: 'dd_import_gitleaks.sarif'
          so_api_base_url: ${{ vars.SO_API_BASE_URL }}
          so_api_token: ${{ secrets.SO_API_TOKEN }}
          so_product_name: ${{ vars.SO_PRODUCT_NAME }}

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: secobserve
          path: |
            dd_import_bandit.sarif
            dd_import_semgrep.json
            dd_import_kics.sarif
            dd_import_checkov.sarif
            dd_import_trivy_image.json
            dd_import_grype_image.json
            dd_import_gitleaks.sarif
```

##  Examplary pipeline for GitLab CI templates

!!! tip
    The mandatory variables for importing (`SO_API_BASE_URL`, `SO_API_TOKEN` and `SO_PRODUCT_NAME`) can be set as variables in the CI/CD settings of the project in GitLab. Then they don't need to be set in each job.

```yaml
include:
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/DAST/drheader.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/DAST/cryptolyzer.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SAST/bandit.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SAST/checkov.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SAST/eslint.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SAST/kics.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SAST/semgrep.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SCA/grype_image.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SCA/trivy_filesystem.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/SCA/trivy_image.yml"
  - "https://raw.githubusercontent.com/MaibornWolff/secobserve_actions_templates/main/templates/secrets/gitleaks.yml"

grype_image_backend:
  extends: .grype_image
  variables:
    TARGET: "$BACKEND_IMAGE_FULL_NAME_BRANCH"
    REPORT_NAME: "grype_backend_image.json"
    SO_ORIGIN_SERVICE: "backend"

grype_image_frontend:
  extends: .grype_image
  variables:
    TARGET: "$FRONTEND_IMAGE_FULL_NAME_BRANCH"
    REPORT_NAME: "grype_frontend_image.json"
    SO_ORIGIN_SERVICE: "frontend"

trivy_image_backend:
  extends: .trivy_image
  variables:
    TARGET: "$BACKEND_IMAGE_FULL_NAME_BRANCH"
    REPORT_NAME: "trivy_backend_image.json"
    SO_ORIGIN_SERVICE: "backend"

trivy_image_frontend:
  extends: .trivy_image
  variables:
    TARGET: "$FRONTEND_IMAGE_FULL_NAME_BRANCH"
    REPORT_NAME: "trivy_frontend_image.json"
    SO_ORIGIN_SERVICE: "frontend"

trivy_filesystem_frontend:
  extends: .trivy_filesystem
  variables:
    TARGET: "frontend/package-lock.json"
    REPORT_NAME: "trivy_frontend_npm.json"
    SO_ORIGIN_SERVICE: "frontend"
  needs: []

bandit_backend:
  extends: .bandit
  variables:
    TARGET: "backend"
    REPORT_NAME: "bandit_backend.sarif"
    SO_ORIGIN_SERVICE: "backend"
  needs: []

eslint_frontend:
  extends: .eslint
  variables:
    RUN_DIRECTORY: "frontend"
    TARGET: "src"
    REPORT_NAME: "eslint_frontend.sarif"
    SO_ORIGIN_SERVICE: "frontend"
  needs: []

semgrep_backend:
  extends: .semgrep
  variables:
    CONFIGURATION: "r/python"
    TARGET: "backend"
    REPORT_NAME: "semgrep_backend.json"
    SO_ORIGIN_SERVICE: "backend"
  needs: []

semgrep_frontend:
  extends: .semgrep
  variables:
    CONFIGURATION: "r/typescript"
    TARGET: "frontend/src"
    REPORT_NAME: "semgrep_frontend.json"
    SO_ORIGIN_SERVICE: "frontend"
  needs: []

gitleaks:
  extends: .gitleaks
  variables:
    REPORT_NAME: "gitleaks.sarif"
  needs: []


checkov:
  extends: .checkov
  variables:
    TARGET: "."
    REPORT_NAME: "checkov.sarif"
  needs: []

kics:
  extends: .kics
  variables:
    TARGET: "."
    REPORT_NAME: "kics.sarif"
  needs: []

drheader:
  extends: .drheader
  variables:
    TARGET: "https://secobserve.example.com"
    REPORT_NAME: "drheader.json"
    SO_ORIGIN_ENDPOINT_URL: "https://secobserve.example.com"
needs: []

cryptolyzer:
  extends: .cryptolyzer
  variables:
    TARGET: "secobserve.example.com"
    REPORT_NAME: "cryptolyzer.json"
  needs: []
```
