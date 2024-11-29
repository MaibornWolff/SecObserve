import ApprovalIcon from "@mui/icons-material/Approval";
import CancelIcon from "@mui/icons-material/Cancel";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { ASSESSMENT_STATUS_CHOICES } from "../types";

const AssessmentBulkApproval = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const { selectedIds } = useListContext();
    const unselectAll = useUnselectAll("observation_logs");
    const [loading, setLoading] = useState(false);

    const assessmentUpdate = async (data: any) => {
        setLoading(true);
        const patch = {
            assessment_status: data.assessment_status,
            approval_remark: data.approval_remark,
            observation_logs: selectedIds,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/observation_logs/bulk_approval/", {
            method: "PATCH",
            body: JSON.stringify(patch),
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                notify("Assessments updated", {
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

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton />
            <SaveButton />
        </Toolbar>
    );
    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<ApprovalIcon />}
            >
                Approval
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle sx={{ display: "flex", alignItems: "center" }}>
                    <ApprovalIcon />
                    &nbsp;&nbsp;Assessment approval
                </DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={assessmentUpdate} toolbar={<CustomToolbar />}>
                        <AutocompleteInputMedium
                            source="assessment_status"
                            choices={ASSESSMENT_STATUS_CHOICES}
                            validate={validate_required}
                            label="Decision"
                        />
                        <TextInputWide source="approval_remark" validate={validate_required_255} label="Remark" />
                    </SimpleForm>
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

export default AssessmentBulkApproval;
