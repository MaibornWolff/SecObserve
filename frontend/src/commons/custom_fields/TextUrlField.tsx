import LaunchIcon from "@mui/icons-material/Launch";
import { Fragment } from "react";

import { useStyles } from "../../commons/layout/themes";

interface TextUrlFieldProps {
    text: string | number;
    url: string;
    label: string;
}

function is_valid_url(urlString: string): boolean {
    const SAFE_URL_PATTERN = /^(?:(?:https?|mailto|ftp|tel|file|sms):|[^&:/?#]*(?:[/?#]|$))/gi;

    try {
        return Boolean(new URL(urlString) && urlString.match(SAFE_URL_PATTERN));
    } catch (e) {
        return false;
    }
}

function is_valid_relative_url(urlString: string): boolean {
    const RELATIVE_PATTERN = /^#\/.*$/gi;

    try {
        return Boolean(urlString.match(RELATIVE_PATTERN));
    } catch (e) {
        return false;
    }
}

function is_invalid_url(urlString: string): boolean {
    return !is_valid_url(urlString) && !is_valid_relative_url(urlString);
}

const TextUrlField = (props: TextUrlFieldProps) => {
    const { classes } = useStyles();

    return (
        <Fragment>
            {is_valid_url(props.url) && (
                <a
                    href={props.url} // nosemgrep: typescript.react.security.audit.react-href-var.react-href-var
                    // nosemgrep because is_valid_url() sanitizes the url
                    target="_blank"
                    rel="noreferrer"
                    className={classes.link}
                    style={{
                        fontSize: "0.875rem",
                        fontFamily: "Roboto",
                        lineHeight: 1.43,
                    }}
                >
                    {props.text} &nbsp;
                    <LaunchIcon sx={{ fontSize: "0.8rem" }} />
                </a>
            )}
            {is_valid_relative_url(props.url) && (
                <a
                    href={props.url} // nosemgrep: typescript.react.security.audit.react-href-var.react-href-var
                    // nosemgrep because is_valid_url() sanitizes the url
                    className={classes.link}
                    style={{
                        fontSize: "0.875rem",
                        fontFamily: "Roboto",
                        lineHeight: 1.43,
                    }}
                >
                    {props.text}
                </a>
            )}
            {is_invalid_url(props.url) && (
                <span
                    style={{
                        fontSize: "0.875rem",
                        fontFamily: "Roboto",
                        lineHeight: 1.43,
                    }}
                >
                    {props.text}
                </span>
            )}
        </Fragment>
    );
};

TextUrlField.defaultProps = { label: "" };

export default TextUrlField;
