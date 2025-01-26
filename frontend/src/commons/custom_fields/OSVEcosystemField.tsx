import { Typography } from "@mui/material";
import { Fragment } from "react";

interface OSVEcosystemFieldProps {
    osv_linux_ecosystem: string | undefined;
    osv_linux_release: string | undefined;
    label: string;
}

const OSVEcosystemField = (props: OSVEcosystemFieldProps) => {
    return (
        <Fragment>
            {props.osv_linux_ecosystem && props.osv_linux_release && (
                <Typography variant="body2">
                    {props.osv_linux_ecosystem}:{props.osv_linux_release}
                </Typography>
            )}
            {props.osv_linux_ecosystem && !props.osv_linux_release && (
                <Typography variant="body2">{props.osv_linux_ecosystem}</Typography>
            )}
        </Fragment>
    );
};

export default OSVEcosystemField;
