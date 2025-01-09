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
    unsaved_license: str


@dataclass
class Metadata:
    scanner: str
    container_name: str
    container_tag: str
    container_digest: str
    file: str
