import DeleteIcon from "@mui/icons-material/Delete";
import { Backdrop, CircularProgress } from "@mui/material";
import { useState } from "react";
import { Button, Confirm, useDeleteMany, useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

const ObservationBulkDeleteButton = () => {
    const [open, setOpen] = useState(false);
    const [deleted, setDeleted] = useState(false);
    const [error_shown, setErrorShown] = useState(false);
    const [deleteMany, { isLoading, error }] = useDeleteMany();
    const { selectedIds } = useListContext();
    const refresh = useRefresh();
    const notify = useNotify();
    const unselectAll = useUnselectAll("observations");
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        deleteMany("observations", { ids: selectedIds });
        setDeleted(true);
        refresh();
        unselectAll();
        setOpen(false);
    };

    if (error && !error_shown) {
        setErrorShown(true);
        setDeleted(false);
        notify("Some observations could not be deleted: " + error, {
            type: "warning",
        });
    } else if (deleted) {
        setDeleted(false);
        notify("Observations deleted");
    }

    return (
        <>
            <Button label="Delete" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open && !isLoading}
                title="Delete Observations"
                content="Are you sure you want to delete the selected observations?"
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
            {isLoading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </>
    );
};

export default ObservationBulkDeleteButton;
