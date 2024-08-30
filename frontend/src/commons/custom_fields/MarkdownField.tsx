import Markdown from "markdown-to-jsx";

import { useLinkStyles } from "../../commons/layout/themes";
import { getSettingTheme } from "../user_settings/functions";

interface MarkdownProps {
    content: string;
    label: string;
}

const MarkdownField = (props: MarkdownProps) => {
    const { classes } = useLinkStyles({ setting_theme: getSettingTheme() });

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

export default MarkdownField;
