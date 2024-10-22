import DeleteIcon from "@mui/icons-material/Delete";
import { Backdrop, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Button, Confirm, useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type LicenseComponentBulkDeleteButtonProps = {
    product: any;
};

const LicenseComponentBulkDeleteButton = (props: LicenseComponentBulkDeleteButtonProps) => {
    const [open, setOpen] = useState(false);
    const { selectedIds } = useListContext();
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const unselectAll = useUnselectAll("components");
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        setLoading(true);
        const url =
            window.__RUNTIME_CONFIG__.API_BASE_URL +
            "/products/" +
            props.product.id +
            "/license_components_bulk_delete/";
        const delete_data = {
            components: selectedIds,
        };

        httpClient(url, {
            method: "POST",
            body: JSON.stringify(delete_data),
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                notify("License components deleted", {
                    type: "success",
                });
            })
            .catch((error) => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    return (
        <>
            <Button label="Delete" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open && !loading}
                title="Delete License Components"
                content="Are you sure you want to delete the selected license components?"
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

export default LicenseComponentBulkDeleteButton;
