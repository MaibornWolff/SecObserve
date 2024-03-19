import logging

from application.import_observations.parsers.cyclone_dx.types import Component

logger = logging.getLogger("secobserve.import_observations.cyclone_dx.dependencies")


def get_component_dependencies(data, components, component):
    component_dependencies: list[dict[str, str | list[str]]] = []
    _filter_component_dependencies(
        component.bom_ref,
        data.get("dependencies", []),
        component_dependencies,
    )
    observation_component_dependencies = ""
    translated_component_dependencies = []
    if component_dependencies:
        translated_component_dependencies = _translate_component_dependencies(
            component_dependencies, components
        )

        observation_component_dependencies = "\n".join(
            _get_dependencies(
                f"{component.name}:{component.version}",
                translated_component_dependencies,
            )
        )

    return observation_component_dependencies, translated_component_dependencies


def _filter_component_dependencies(
    bom_ref: str,
    dependencies: list[dict[str, str | list[str]]],
    component_dependencies: list[dict[str, str | list[str]]],
) -> None:
    for dependency in dependencies:
        if dependency in component_dependencies:
            continue
        depends_on = dependency.get("dependsOn", [])
        if bom_ref in depends_on:
            component_dependencies.append(dependency)
            _filter_component_dependencies(
                str(dependency.get("ref")), dependencies, component_dependencies
            )


def _translate_component_dependencies(
    component_dependencies: list[dict[str, str | list[str]]],
    components: dict[str, Component],
) -> list[dict]:
    translated_component_dependencies = []

    for component_dependency in component_dependencies:
        translated_component_dependency: dict[str, str | list[str]] = {}

        translated_component_dependency["ref"] = _get_bom_ref_name_version(
            str(component_dependency.get("ref")), components
        )

        translated_component_dependencies_inner: list[str] = []
        for dependency in component_dependency.get("dependsOn", []):
            translated_component_dependencies_inner.append(
                _get_bom_ref_name_version(dependency, components)
            )
        translated_component_dependencies_inner.sort()
        translated_component_dependency["dependsOn"] = (
            translated_component_dependencies_inner
        )

        translated_component_dependencies.append(translated_component_dependency)

    return translated_component_dependencies


def _get_bom_ref_name_version(bom_ref: str, components: dict[str, Component]) -> str:
    component = components.get(bom_ref, None)
    if not component:
        return ""

    if component.version:
        component_name_version = f"{component.name}:{component.version}"
    else:
        component_name_version = component.name

    return component_name_version


def _get_dependencies(
    component_version: str,
    translated_component_dependencies: list[dict],
) -> list[str]:
    roots = _get_roots(translated_component_dependencies)
    dependencies: list[str] = []
    try:
        for root in roots:
            dependencies += _get_dependencies_recursive(
                root, root, component_version, translated_component_dependencies
            )
    except RecursionError as e:
        logger.warning(e)
        return []

    return_dependencies = []
    for dependency in dependencies:
        if dependency and dependency.endswith(component_version):
            return_dependencies.append(dependency)

    return return_dependencies


def _get_dependencies_recursive(
    root: str,
    initial_dependency: str,
    component_version: str,
    translated_component_dependencies: list[dict],
) -> list[str]:
    dependencies = []
    for dependency in translated_component_dependencies:
        ref = dependency.get("ref")
        if ref == root:
            for dependant in dependency.get("dependsOn", []):
                new_dependency = f"{initial_dependency} --> {dependant}"
                if dependant == component_version:
                    dependencies.append(new_dependency)
                else:
                    new_dependencies = _get_dependencies_recursive(
                        dependant,
                        new_dependency,
                        component_version,
                        translated_component_dependencies,
                    )
                    dependencies += new_dependencies

    return dependencies


def _get_roots(
    translated_component_dependencies: list[dict],
) -> list[str]:
    roots = []
    for dependency in translated_component_dependencies:
        ref = dependency.get("ref")
        if not ref:
            continue
        if not any(
            ref in d.get("dependsOn", []) for d in translated_component_dependencies
        ):
            roots.append(ref)

    return roots
