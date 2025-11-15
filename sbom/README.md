# Software Bill of Materials (SBOM)

This directory contains the CycloneDX SBOMs for the project of the last 3 releases (starting with release 1.8). The set of SBOMs consists of the following files:

* `sbom_backend_application_RELEASE.json` - Python libraries of the backend application, derived from [../backend/poetry.lock](../backend/poetry.lock)
* `sbom_frontend_application_RELEASE.json` - NPM libraries of the frontend application, derived from [../frontend/package-lock.json](../frontend/package-lock.json)
* `sbom_backend_container_RELEASE.json` - Operating system components of the backend container, derived from [backend container image of the release](https://github.com/SecObserve/SecObserve/pkgs/container/secobserve-backend)
* `sbom_frontend_container_RELEASE.json` - Operating system components of the frontend container, derived from [frontend container image of the release](https://github.com/SecObserve/SecObserve/pkgs/container/secobserve-frontend)
* `sbom_RELEASE.json` - Combined SBOM of the backend and frontend applications and containers


## Minimum requirements for content

* `metadata/component` 
    * name
    * version
    * description
    * supplier
    * purl
    * license (for application SBOMs)
* `components`
    * name
    * version
    * purl
    * licenses
    * type
* `dependencies`
    * hierarchical dependencies, starting from the `metadata/component`


## Design decisions

* **Split into 4 SBOMs**
    * Backend and frontend could be installed separately
    * Backend and frontend could be installed without using the docker images
    * Backend container does not contain hierarchy of Python libraries
    * Frontend container does not contain identifiable NPM libraries, because of the `vite` build process
* **Merge into combined SBOM**
    * For a complete overview of the applications and containers
* **Automated generation by GitHub workflow [generate_sboms.yml](../.github/workflows/generate_sboms.yml)**
    * Tracebility of SBOM content to the source files

