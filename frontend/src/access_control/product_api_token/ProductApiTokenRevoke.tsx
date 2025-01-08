import { useState } from "react";
import { Confirm, useNotify, useRefresh } from "react-admin";

import RemoveButton from "../../commons/custom_fields/RemoveButton";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

type RevokeProductApiTokenProps = {
    product: any;
};

const RevokeProductApiToken = (props: RevokeProductApiTokenProps) => {
    const refresh = useRefresh();
    const notify = useNotify();

    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const handleApiTokenRevoke = async () => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/product_api_tokens/" + props.product.id + "/";
        httpClient(url, {
            method: "DELETE",
        })
            .then(() => {
                notify("Product API token revoked", {
                    type: "success",
                });
                refresh();
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });

        setOpen(false);
    };

    return (
        <>
            <RemoveButton title="Revoke" onClick={handleOpen} />
            <Confirm
                isOpen={open}
                title="Revoke product API token"
                content={"Are you sure you want to revoke the product API token?"}
                onConfirm={handleApiTokenRevoke}
                onClose={handleClose}
            />
        </>
    );
};

export default RevokeProductApiToken;
