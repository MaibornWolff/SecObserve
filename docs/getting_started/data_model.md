# Data model

``` mermaid
erDiagram
    Product_Group |o--o{ Product : has
    Product ||--o{ Observation : has
    Product ||--o{ Branch_Version : has
    Product ||--o{ Service : has
    Product ||--o{ Vulnerability_Check : has
    Product ||--o{ Product_Rule : has
    Product ||--o{ API_Configuration : has
    Product ||--o{ Product_Member : has
    Parser ||--o{ Observation: discovered_by
    Observation }o--o| Branch_Version: found_in
    Observation ||--|{ Observation_Log : has
    Observation ||--|{ Reference : has
    Observation ||--|{ Evidence : has
    General_Rule
```

## Product Group

A `Product Group` is a collection of products. It is used to group products that belong together, e.g. because they are part of the same project. In the database, the product groups are stored in the table `Product` with the flag `is_product_group` set to `true`.

## Product

A `Product` is the representation of the system that is checked for vulnerabilities.

## Observation

An `Observation` is something that has been discovered by a vulnerability scanner. Not every observation is actually a vulnerability. An assessment can show it is e.g. a false positive or not applicable in the current context.

Every `Observation` belongs to exactly one product.

## Branch / Version

Software development often uses branches in the source code repository and software is often available in multiple versions. Vulnerability scanners can run for different branches / versions of a product and observations can be viewed and managed by branch / version. See more in [branches and Versions](../usage/branches.md).

## Service

A `Service` is a self-contained piece of functionality of a product. Can be something like a microservice or `backend` or `frontend`.	

## Vulnerability Check

An import for one product, one branch / version and one file name resp. one API configuration is a so-called vulnerability check. See more in [Import algorithm](../usage/import_observations.md#import-algorithm).

## Parser

SecObserve can parse a variety of data formats, written by vulnerability scanners. Besides file-based parsers, SecObserve implements API-based parsers as well, which get data directly from a system via REST calls. See more about vulnerability scanners and parsers on [Supported scanners](../integrations/supported_scanners.md).

## Observation Log

Every change of the severity or the status of an observation is recorded in the `Observation Log`.

## Reference

`References` are links to further information about the observation. They are imported with the observation.

## Evidence

`Evidences` are extracts from the scan reports showing the basis on which the observation was created.

## Product Rule / General Rule

Rules can change the severity or the status of an observation can be changed during the import. An example would be to set a risk acceptance automatically for observations that shall not be fixed. `General Rules` will be applied for all products, while `Product Rules` are only valid for one product. See more about rules on [Rule engine](../usage/rule_engine.md).

## API Configuration

Parsers who get data from vulnerability scanners via a REST API need a configuration how to access the API (URL, API key, ...). The `API Configuration` is set per product.

## Product Member

`Product Members` define who has access to a product. Depending on the role of a user for a product, they have more or less functionality available, see more on [Users and permissions](../usage/users_permissions.md).
