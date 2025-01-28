from collections import defaultdict

# These functions are still needed for migration 0051_convert_origin_component_dependencies


def _parse_mermaid_graph_content(
    mermaid_graph_content: list[str],
) -> dict[str, set[str]]:
    graph = defaultdict(set)

    for line in mermaid_graph_content:
        parts = line.strip().split("-->")
        parts = [part.strip() for part in parts]
        for i in range(len(parts) - 1):
            graph[parts[i]].add(parts[i + 1])

    return graph


def _generate_dependency_list_as_text(graph: dict[str, set[str]]) -> str:
    lines = []
    for src, dests in graph.items():
        for dest in sorted(dests):
            lines.append(f"{src} --> {dest}")
    return "\n".join(lines)
