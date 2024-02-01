import CancelIcon from "@mui/icons-material/Cancel";
import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";

import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";

const ObservationAssessment = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const observationUpdate = async (data: any) => {
        const patch = {
            severity: data.current_severity,
            status: data.current_status,
            comment: data.comment,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/observations/" + data.id + "/assessment/", {
            method: "PATCH",
            body: JSON.stringify(patch),
        })
            .then(() => {
                refresh();
                notify("Observation updated", {
                    type: "success",
                });
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });

        setOpen(false);
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
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Observation Assessment</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <AutocompleteInputMedium
                            source="current_severity"
                            choices={OBSERVATION_SEVERITY_CHOICES}
                            validate={validate_required}
                        />
                        <AutocompleteInputMedium
                            source="current_status"
                            choices={OBSERVATION_STATUS_CHOICES}
                            validate={validate_required}
                        />
                        <TextInputWide source="comment" validate={validate_required_255} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ObservationAssessment;
