import { Typography } from "@mui/material";
import { Fragment } from "react";

interface OSVLinuxDistributionFieldProps {
    osv_linux_distribution: string | undefined;
    osv_linux_release: string | undefined;
    label: string;
}

const OSVLinuxDistributionField = (props: OSVLinuxDistributionFieldProps) => {
    return (
        <Fragment>
            {props.osv_linux_distribution && props.osv_linux_release && (
                <Typography variant="body2">
                    {props.osv_linux_distribution}:{props.osv_linux_release}
                </Typography>
            )}
            {props.osv_linux_distribution && !props.osv_linux_release && (
                <Typography variant="body2">{props.osv_linux_distribution}</Typography>
            )}
        </Fragment>
    );
};

export default OSVLinuxDistributionField;
