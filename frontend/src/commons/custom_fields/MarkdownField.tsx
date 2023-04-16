import Markdown from "markdown-to-jsx";

import { useStyles } from "../../commons/layout/themes";

interface MarkdownProps {
    content: string;
    label: string;
}

const MarkdownField = (props: MarkdownProps) => {
    const { classes } = useStyles();

    return (
        <Markdown
            style={{
                fontSize: "0.875rem",
                fontFamily: "Roboto",
                lineHeight: 1.43,
            }}
            options={{
                overrides: {
                    a: {
                        props: {
                            className: classes.link,
                        },
                    },
                },
            }}
        >
            {props.content}
        </Markdown>
    );
};

MarkdownField.defaultProps = { label: "" };

export default MarkdownField;
