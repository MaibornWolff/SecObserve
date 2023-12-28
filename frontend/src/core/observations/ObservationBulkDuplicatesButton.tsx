import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Backdrop, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Button, Confirm, useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type ObservationBulkDuplicatesButtonProps = {
    observation: any;
};

const ObservationBulkDuplicatesButton = (props: ObservationBulkDuplicatesButtonProps) => {
    const [open, setOpen] = useState(false);
    const { selectedIds } = useListContext();
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const unselectAll = useUnselectAll("potential_duplicates");
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        setLoading(true);
        const url =
            window.__RUNTIME_CONFIG__.API_BASE_URL +
            "/products/" +
            props.observation.product_data.id +
            "/observations_bulk_mark_duplicates/";
        const duplicates_data = {
            observation_id: props.observation.id,
            potential_duplicates: selectedIds,
        };

        httpClient(url, {
            method: "POST",
            body: JSON.stringify(duplicates_data),
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                notify("Observations marked as duplicates", {
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
            <Button label="Mark Duplicates" onClick={handleClick} startIcon={<PlaylistAddCheckIcon />} />
            <Confirm
                isOpen={open && !loading}
                title="Mark duplicates"
                content="Are you sure you want to mark the selected observations as duplicates?"
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

export default ObservationBulkDuplicatesButton;
