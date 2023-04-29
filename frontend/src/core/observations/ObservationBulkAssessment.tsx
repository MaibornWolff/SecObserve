import CancelIcon from "@mui/icons-material/Cancel";
import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useListContext,
    useNotify,
    useRefresh,
    useUnselectAll,
} from "react-admin";

import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";

const ObservationBulkAsessment = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const { selectedIds } = useListContext();
    const unselectAll = useUnselectAll("observations");

    const observationUpdate = async (data: any) => {
        const patch = {
            severity: data.current_severity,
            status: data.current_status,
            comment: data.comment,
        };

        let error_message = "";
        let has_error = false;
        for (const index in selectedIds) {
            if (has_error) {
                break;
            }
            httpClient(
                window.__RUNTIME_CONFIG__.API_BASE_URL +
                    "/observations/" +
                    // We trust the selectIds coming from the ListContext
                    // eslint-disable-next-line security/detect-object-injection
                    selectedIds[index] +
                    "/assessment/",
                {
                    method: "PATCH",
                    body: JSON.stringify(patch),
                }
            )
                .then(() => {
                    refresh();
                })
                .catch((error) => {
                    refresh();
                    has_error = true;
                    error_message = error.message;
                });
        }
        if (has_error) {
            notify(error_message, {
                type: "warning",
            });
        } else {
            notify("Observations updated", {
                type: "success",
            });
        }
        unselectAll();
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
                color: "#000000dd",
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
                        <TextInputWide multiline source="comment" validate={requiredValidate} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

const requiredValidate = [required()];

export default ObservationBulkAsessment;
