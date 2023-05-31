import GeneralRuleIcon from "@mui/icons-material/Rule";
import { Backdrop, Button, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Confirm, useNotify, useRefresh } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type ProductRuleApplyProps = {
    product: any;
};

const ProductRuleApply = (props: ProductRuleApplyProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        setLoading(true);
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/products/" + props.product.id + "/apply_rules/";

        httpClient(url, {
            method: "POST",
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                notify("Rules applied", {
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
                variant="contained"
                onClick={handleClick}
                startIcon={<GeneralRuleIcon />}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
            >
                Apply rules
            </Button>
            <Confirm
                isOpen={open && !loading}
                title="Apply rules"
                content={"Are you sure you want to apply all rules to the product " + props.product.name + "?"}
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

export default ProductRuleApply;
