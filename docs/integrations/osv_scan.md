# Vulnerability scanning from OSV database [experimental]

The components of a product can be scanned for vulnerabilities using the OSV database. The OSV database is a database of open-source vulnerabilities, maintained by Google and is available at [https://osv.dev/](https://osv.dev/).

There are 2 preconditions for a product to be met before using the OSV database for vulnerability scanning:

* License information has to be imported, only then all components are available for scanning.
* The flag `OSV scanning enabled` in the product settings has to be activated.

Then  the OSV scan can be started from the `Import` menu. If a branch is selected, the scan will be performed on the components of the branch. If no branch is selected, the scan will be performed on the components of all branches and components without a branch.

OSV delivers vulnerabilities for a component, without regard to the version of the component, plus a list of affected versions. Currently these package managers are supported directly to get the affected versions, by using information from the PURL of the component:

* **bitnami:** Bitnami
* **conan:** ConanCenter
* **cran:** CRAN
* **cargo:** crates.io
* **golang:** Go
* **hackage:** Hackage
* **hex:** Hex
* **maven:** Maven
* **npm:** npm
* **nuget:** NuGet
* **pub:** Pub
* **pypi:** PyPI
* **gem:** RubyGems
* **swift:** SwiftURL

To correctly identify Linux packages, the Linux distribution and version has to be set in the product or branch settings according to [OSV affected package specification](https://ossf.github.io/osv-schema/#affectedpackage-field). If it is not set for a branch, the product settings are used. Examples are:

| Linux distribution | Version   |
|--------------------|-----------|
| Alpine             | v3.21     |
| Ubuntu             | 22.04:LTS |
| Red Hat            | rhel_aus:8.4::appstream |

A regular automated scan for all enabled products is planned for a future release.
