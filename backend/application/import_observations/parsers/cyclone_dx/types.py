from dataclasses import dataclass


@dataclass
class Component:
    bom_ref: str
    name: str
    version: str
    type: str
    purl: str
    cpe: str
    json: dict[str, str]
