# VEX documents

A VEX (Vulnerability Exploitability eXchange) document is a form of a security advisory that indicates whether a product or products are affected by a known vulnerability or vulnerabilities. SecObserve supports the export of VEX documents in two formats:

* The [Common Security Advisory Framework](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html) (CSAF) format is an [OASIS](https://www.oasis-open.org/) standard 
* [OpenVEX](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md) is a community-driven format, maintained by an [OpenSSF](https://openssf.org/) special interest group

## Feature flag

The VEX feature is is disabled by default because not all installations will use it. It can be enabled by setting the feature flag `FEATURE_VEX` in the [Settings](../getting_started/configuration.md#admininistration-in-secobserve):

![VEX feature flag](../assets/images/screenshot_vex_feature_flag.png)

Enabling the feature flag will make the VEX functionality available in the main navigation bar and enable the "VEX justification" field in several places.


## Create a new VEX document

To create a VEX document, the user has to define a set of attributes in a dialog. Some of them are different for either a CSAF or OpenVEX document. Other attributes are common to both formats:

| Attribute             | Optionality | Description |
|-----------------------|:-----------:|-------------|
| `Product`             | optional    | If a product is selected, only vulnerabilities for that product will be included in the VEX document. |
| `Vulnerabilities`     | optional    | Zero or more names of vulnerabilities to be included in the VEX document, e.g. `CVE-2021-44228` |
| `Branches / Versions` | optional    | If a product is selected, the VEX document can be limited to cover only the selected branches / versions of this product. |
| `ID prefix`           | mandatory   | The `ID prefix` is part of of the unique identifier of the VEX document. The unique id has the format `prefix_year_counter`, where the counter is increased by 1 for every new document per prefix and year. This unique id will stored in a designated attribute in the VEX document and used for the filename of the VEX document. |

Either a product or at least one vulnerability has to be selected.

After pushing the **Create** button in the dialog, the VEX document with the version 1 will be created and ready for download. Additionally a database entry with all attributes is created, which can be selected later to create an updated version of the VEX document


## Update a VEX document

After selecting the entry of either a CSAF or OpenVEX document from the respective list, a form shows the details of its attributes and a button to update a document. Some of the attributes can be changed for a new version of the document. If there have been no changes to the included vulnerabilities, no new document will be created. Otherwise a new version of the document will be created and ready for download.
