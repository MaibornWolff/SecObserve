from dataclasses import dataclass
from typing import Optional

from application.core.models import Observation, Product
from application.core.types import PURL_Type
from application.licenses.models import License_Component


@dataclass
class PURLTypeElement:
    id: str
    name: str


@dataclass
class PURLTypeList:
    count: int
    results: list[PURLTypeElement]


def get_purl_type(purl_type_id: str) -> Optional[PURLTypeElement]:
    name = PURL_Type.PURL_TYPE_CHOICES[purl_type_id]
    if name:
        return PURLTypeElement(id=purl_type_id, name=name)

    return None


def get_purl_types(product: Product, for_observations: bool, for_license_components: bool) -> PURLTypeList:
    purl_types = PURLTypeList(
        count=0,
        results=[],
    )

    if for_observations:
        observation_purl_types = (
            Observation.objects.filter(product=product)
            .exclude(origin_component_purl_type="")
            .values("origin_component_purl_type")
            .distinct()
        )
        purl_types = PURLTypeList(
            count=observation_purl_types.count(),
            results=[
                PURLTypeElement(
                    id=purl_type.get("origin_component_purl_type", ""),
                    name=PURL_Type.PURL_TYPE_CHOICES.get(purl_type.get("origin_component_purl_type", ""), ""),
                )
                for purl_type in observation_purl_types
            ],
        )
    elif for_license_components:
        license_component_purl_types = (
            License_Component.objects.filter(product=product)
            .exclude(component_purl_type="")
            .values("component_purl_type")
            .distinct()
        )
        purl_types = PURLTypeList(
            count=license_component_purl_types.count(),
            results=[
                PURLTypeElement(
                    id=purl_type.get("component_purl_type", ""),
                    name=PURL_Type.PURL_TYPE_CHOICES.get(purl_type.get("component_purl_type", ""), ""),
                )
                for purl_type in license_component_purl_types
            ],
        )

    return purl_types
