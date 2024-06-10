import CancelIcon from "@mui/icons-material/Cancel";
import DeleteIcon from "@mui/icons-material/Delete";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

const AssessmentDeleteApproval = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const { selectedIds } = useListContext();
    const unselectAll = useUnselectAll("observation_logs");
    const [loading, setLoading] = useState(false);

    const assessmentDelete = async () => {
        setLoading(true);
        const deleteBody = {
            observation_logs: selectedIds,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/observation_logs/bulk_delete/", {
            method: "DELETE",
            body: JSON.stringify(deleteBody),
        })
            .then((response) => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                const count = response.json.count;
                notify(`${count} assessment${count === 1 ? "" : "s"} deleted`, {
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

    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const handleCancel = () => setOpen(false);

    const handleOpen = () => setOpen(true);

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
            }}
            variant="contained"
            onClick={handleCancel}
            color="inherit"
            startIcon={<CancelIcon />}
        >
            Cancel
        </Button>
    );

    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<DeleteIcon />}
            >
                Delete
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle sx={{ display: "flex", alignItems: "center" }}>
                    <DeleteIcon />
                    &nbsp;&nbsp;Delete assessments
                </DialogTitle>
                <DialogContent>
                    <p>Are you sure you want to delete the selected assessments?</p>
                    <CancelButton />
                    <Button onClick={assessmentDelete} variant="contained" color="primary">
                        Confirm deletion
                    </Button>
                </DialogContent>
            </Dialog>
            {loading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </Fragment>
    );
};

export default AssessmentDeleteApproval;
