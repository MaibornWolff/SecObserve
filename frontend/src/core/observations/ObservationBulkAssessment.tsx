import CancelIcon from "@mui/icons-material/Cancel";
import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, useListContext, useNotify, useRefresh, useUnselectAll } from "react-admin";

import { validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";

type ObservationBulkAssessmentButtonProps = {
    product: any;
};

const ObservationBulkAssessment = (props: ObservationBulkAssessmentButtonProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const { selectedIds } = useListContext();
    const unselectAll = useUnselectAll("observations");

    const observationUpdate = async (data: any) => {
        setLoading(true);
        const url =
            window.__RUNTIME_CONFIG__.API_BASE_URL + "/products/" + props.product.id + "/observations_bulk_assessment/";
        const assessment_data = {
            severity: data.current_severity,
            status: data.current_status,
            comment: data.comment,
            observations: selectedIds,
        };

        httpClient(url, {
            method: "POST",
            body: JSON.stringify(assessment_data),
        })
            .then(() => {
                refresh();
                setOpen(false);
                setLoading(false);
                unselectAll();
                notify("Observations updated", {
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
                startIcon={<PlaylistAddCheckIcon />}
            >
                Assessment
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Bulk Observation Assessment</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <AutocompleteInputMedium
                            source="current_severity"
                            label="Severity"
                            choices={OBSERVATION_SEVERITY_CHOICES}
                        />
                        <AutocompleteInputMedium
                            source="current_status"
                            label="Status"
                            choices={OBSERVATION_STATUS_CHOICES}
                        />
                        <TextInputWide source="comment" validate={validate_required_255} />
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

export default ObservationBulkAssessment;
