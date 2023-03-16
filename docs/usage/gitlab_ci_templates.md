# GitLab CI templates

Integrating vulnerability scanners in a CI/CD pipeline can be cumbersome. Every tool is different to install and has different parameters. Our repository of GitLab CI templates makes this process very straightforward, with a unified way to start the tools. The tools in the template repository will be updated regularly, so that all the latest features and bugfixes are available.

All templates run the scanner, import the results into SecObserve and make the report available as an artifact.

## Variables

Most of the templates use the same set of variables:

| Variable | Optionality | Description |
|----------|-------------|-------------|
| **Scanning** |
| `TARGET` | *mandatory* | The target to be scanned, often it is a path of the filesystem, but can be a Docker image, an URL or others. |
| `REPORT_NAME` | *mandatory* | The name of the report to be written. It will be saved as an artifact. |
| `RUN_DIRECTORY` | *optional* | The directory where to run the scanner, only to be used when the `TARGET` is a path. |
| `FURTHER_PARAMETERS` | *optional* | Further parameters to be given to the scanner. |
| `CONFIGURATION` | *mandatory, only for Semgrep* | Configuration to be used with Semgrep. |
| `RULES` | *optional, only for DrHeader* | Custom rules to be used with DrHeader. |
| **Importing** |
| `SO_UPLOAD` | *optional* | No upload of observations into SecObserve if value is not `true`, default is `true`. |
| `SO_API_BASE_URL` | *mandatory* | Base URL of the SecObserve backend, e.g. `https://secobserve-backend.example.com`. |
| `SO_API_TOKEN` | *mandatory* | API token of the user to be used for the import. The users needs at least the `Upload` role. |
| `SO_PRODUCT_NAME` | *mandatory* | Name of the product which observations are imported. The product has to exist before starting the import. |
| `SO_PARSER_NAME` | *optional* | Name of the parser to read the import file or import API. It is set by the template. |
| `SO_FILE_NAME` | *optional* | Name of file for file-based parsers, default is `REPORT_NAME`.|
| `SO_API_CONFIGURATION_NAME` | *optional* | Name of API configuration for API-based parsers. |
| `SO_ORIGIN_SERVICE` | *optional* | Service name to be set for all imported observations. |
| `SO_ORIGIN_DOCKER_IMAGE_NAME_TAG` | *optional* | Name:Tag of Docker image to be set for all imported observations. |
| `SO_ORIGIN_ENDPOINT_URL` | *optional* | URL of endpoint to be set for all imported observations. |


## Supported scanners

| Template | Scanner | File format | `TARGET` |
|----------|---------|-------------|--------|
| `templates/SCA/grype_image.yml` | [Grype](https://github.com/anchore/grype) | CycloneDX | Docker image |
| `templates/SCA/trivy_filesystem.yml` | [Trivy](https://aquasecurity.github.io/trivy) | CycloneDX | Path |
| `templates/SCA/trivy_image.yml` | [Trivy](https://aquasecurity.github.io/trivy) | CycloneDX | Docker image |
| `templates/SAST/bandit.yml` | [Bandit](https://bandit.readthedocs.io/en/latest) | SARIF | Path |
| `templates/SAST/eslint.yml` | [ESLint](https://github.com/nodesecurity/eslint-plugin-security) | SARIF | Path |
| `templates/SAST/semgrep.yml` | [Semgrep](https://semgrep.dev/docs) | Semgrep |Path |
| `templates/SAST/checkov.yml` | [Checkov](https://www.checkov.io/1.Welcome/Quick%20Start.html) | SARIF | Path |
| `templates/SAST/kics.yml` | [KICS](https://docs.kics.io/latest) | SARIF | Path |
| `templates/SAST/trivy_config_secrets.yml` | [Trivy](https://aquasecurity.github.io/trivy) | SARIF | Path |
| `templates/secrets/gitleaks.yml` | [Gitleaks](https://gitleaks.io) | Gitleaks | Path |
| `templates/DAST/drheader.yml` | [DrHeader](https://github.com/Santandersecurityresearch/DrHeader) | DrHeader | URL |
| `templates/DAST/sslyze.yml` | [SSLyze](https://github.com/nabla-c0d3/sslyze) | SSLyze | Hostname |

## Examplary pipeline

!!! tip
    The mandatory variables for importing (`SO_API_BASE_URL`, `SO_API_TOKEN` and `SO_PRODUCT_NAME`) can be set as variables in the CI/CD settings of the project in GitLab. Then they don't need to be set in each job.

```yaml
include:
  - project: "department-csec/secobserve/secobserve_gitlab_includes"
    ref: dev
    file:
      - "templates/SCA/grype_image.yml"
      - "templates/SCA/trivy_filesystem.yml"
      - "templates/SCA/trivy_image.yml"
      - "templates/SAST/bandit.yml"
      - "templates/SAST/checkov.yml"
      - "templates/SAST/eslint.yml"
      - "templates/SAST/kics.yml"
      - "templates/SAST/semgrep.yml"
      - "templates/SAST/trivy_config_secrets.yml"
      - "templates/secrets/gitleaks.yml"
      - "templates/DAST/drheader.yml"
      - "templates/DAST/sslyze.yml"

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

sslyze:
  extends: .sslyze
  variables:
    TARGET: "secobserve.example.com"
    REPORT_NAME: "sslyze.json"
  needs: []
```
