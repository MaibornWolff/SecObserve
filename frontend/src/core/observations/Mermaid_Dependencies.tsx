import CloseIcon from "@mui/icons-material/Close";
import { Dialog, DialogContent, DialogTitle, Divider, IconButton, Stack } from "@mui/material";
import mermaid from "mermaid";
import { Fragment, useEffect, useState } from "react";
import { Labeled, WrapperField, useRecordContext } from "react-admin";

import LabeledTextField from "../../commons/custom_fields/LabeledTextField";
import { getTheme } from "../../commons/user_settings/functions";

mermaid.initialize({
    flowchart: {
        padding: 10,
    },
});

const GraphSVG = () => {
    const svg = document.querySelector(".mermaid svg");
    if (svg == null) {
        return <Fragment />;
    }
    const svgData = new XMLSerializer().serializeToString(svg);
    const blob = new Blob([svgData], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    console.log(url);
    return <img src={url} alt="Component dependency graph not available" />;
};

const createMermaidGraph = (dependencies_str: string) => {
    const dependencies = dependencies_str.split("\n");
    if (dependencies.length == 0) {
        return "Error: No dependencies found";
    }
    if (dependencies.length > 500) {
        return "Error: Graph is too large, it has more than 500 dependencies";
    }
    const line_color = getTheme() == "dark" ? "white" : "black";
    const primary_color = getTheme() == "dark" ? "#0086B4" : "#C9F1FF";
    const primary_text_color = getTheme() == "dark" ? "white" : "black";
    let mermaid_content =
        "---\n" +
        "  config:\n" +
        "    theme: base\n" +
        "    themeVariables:\n" +
        '      primaryColor: "'.concat(primary_color).concat('"\n') +
        '      primaryBorderColor: "'.concat(primary_color).concat('"\n') +
        "      primaryTextColor: ".concat(primary_text_color).concat("\n") +
        "      lineColor: ".concat(line_color).concat("\n") +
        "      fontFamily: Roboto\n" +
        "      fontSize: 0.875rem\n" +
        "---\n" +
        "flowchart LR\n";

    const components = new Set<string>();
    for (const dependency of dependencies) {
        const components_list = dependency.split(" --> ");
        if (components_list.length != 2) {
            continue;
        }
        components.add(dependency.split(" --> ")[0]);
        components.add(dependency.split(" --> ")[1]);
        mermaid_content += "    " + dependency + "\n";
    }

    let i = 1;
    for (const component of components) {
        mermaid_content = mermaid_content.replaceAll(component + " ", "id" + i.toString() + '("' + component + '") ');
        mermaid_content = mermaid_content.replaceAll(" " + component, " id" + i.toString() + '("' + component + '")');
        i++;
    }

    return mermaid_content;
};

const MermaidDependencies = () => {
    const [open, setOpen] = useState(false);
    const handleOpen = () => {
        setOpen(true);
    };
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const observation = useRecordContext();

    useEffect(() => {
        if (observation) {
            if (document.getElementById("mermaid-dependencies")) {
                document.getElementById("mermaid-dependencies")?.removeAttribute("data-processed");
                if (!document.getElementById("mermaid-dependencies")?.hasChildNodes()) {
                    mermaid.contentLoaded();
                }
            } else {
                mermaid.contentLoaded();
            }
        }
    }, [observation && observation.origin_component_dependencies, mermaid.contentLoaded()]); // eslint-disable-line react-hooks/exhaustive-deps

    return (
        <Fragment>
            {observation && !createMermaidGraph(observation.origin_component_dependencies).startsWith("Error") && (
                <Fragment>
                    <Labeled sx={{ width: "100%", marginTop: 2 }}>
                        <WrapperField label="Component dependency graph">
                            <div
                                id="mermaid-dependencies"
                                className="mermaid"
                                onClick={handleOpen}
                                style={{ cursor: "pointer" }}
                            >
                                {createMermaidGraph(observation.origin_component_dependencies)}
                            </div>
                        </WrapperField>
                    </Labeled>
                    <Dialog open={open} onClose={handleClose} fullScreen={true}>
                        <DialogTitle>
                            <Stack direction="column" spacing={2}>
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}
                                >
                                    Component dependency graph
                                    <IconButton
                                        sx={{ ml: "auto" }}
                                        onClick={(event) => handleClose(event, "closeButtonClick")}
                                    >
                                        <CloseIcon />
                                    </IconButton>
                                </Stack>
                                <Divider />
                            </Stack>
                        </DialogTitle>
                        <DialogContent>
                            <GraphSVG />
                        </DialogContent>
                    </Dialog>
                </Fragment>
            )}
            {observation && createMermaidGraph(observation.origin_component_dependencies).startsWith("Error") && (
                <Labeled sx={{ width: "100%", marginTop: 2 }}>
                    <LabeledTextField
                        label="Component dependency graph"
                        text={createMermaidGraph(observation.origin_component_dependencies)}
                    />
                </Labeled>
            )}
        </Fragment>
    );
};

export default MermaidDependencies;
