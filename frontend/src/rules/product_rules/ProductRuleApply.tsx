import { useState } from "react";
import { Confirm, useNotify, useRefresh } from "react-admin";
import GeneralRuleIcon from "@mui/icons-material/Rule";
import { Button } from "@mui/material";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type ProductRuleApplyProps = {
    product: any;
};

const ProductRuleApply = (props: ProductRuleApplyProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        const url =
        window.__RUNTIME_CONFIG__.API_BASE_URL +
            "/products/" +
            props.product.id +
            "/apply_rules/";

        httpClient(url, {
            method: "PUT",
        })
            .then(() => {
                notify("Rules applied", {
                    type: "success",
                });
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });

        refresh();
        setOpen(false);
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
                isOpen={open}
                title="Apply rules"
                content={
                    "Are you sure you want to apply all rules to the product " +
                    props.product.name +
                    "?"
                }
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default ProductRuleApply;
