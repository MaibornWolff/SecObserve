import License_Policy_Icon from "@mui/icons-material/Policy";
import { Backdrop, Button, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Confirm, useNotify, useRefresh } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type LicensePolicyApplyProps = {
    license_policy: any;
};

const LicensePolicyApply = ({ license_policy }: LicensePolicyApplyProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        setLoading(true);
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policies/" + license_policy.id + "/apply/";

        httpClient(url, {
            method: "POST",
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                notify("License policy applied", {
                    type: "success",
                });
            })
            .catch((error) => {
                refresh();
                setOpen(false);
                setLoading(false);
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    return (
        <>
            <Button
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                onClick={handleClick}
                startIcon={<License_Policy_Icon />}
            >
                Apply
            </Button>
            <Confirm
                isOpen={open && !loading}
                title="Apply license policy"
                content={
                    "Are you sure you want to apply the license policy " + license_policy.name + " to all products?"
                }
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
            {loading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </>
    );
};

export default LicensePolicyApply;
