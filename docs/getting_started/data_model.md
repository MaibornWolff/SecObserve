# Data model

``` mermaid
erDiagram
    Product ||--o{ Observation : has
    Product ||--o{ Product_Rule : has
    Product ||--o{ API_Configuration : has
    Product ||--o{ Product_Member : has
    Observation }o--|| Parser : discovered_by
    Observation ||--|{ Observation_Log : has
    Observation ||--|{ Reference : has
    Observation ||--|{ Evidence : has
    General_Rule
```

## Product

A `Product` is the representation of the system that is checked for vulnerabilities.

## Observation

An `Observation`  is something that has been discovered by a vulnerability scanner. Not every observation is actually a vulnerability. An assessment can show it is e.g. a false positive or not applicable in the current context.

Every `Observation` belongs to exactly one product.

## Parser

SecObserve can parse a variety of data formats, written by vulnerability scanners. Besides file-based parsers, SecObserve implements API-based parsers as well, which get data directly from a system via REST calls. See more about vulnerability scanners and parsers on [Supported scanners](../usage/supported_scanners.md).

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
