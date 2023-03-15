import * as React from "react";
import {
    SimpleForm,
    required,
    useRefresh,
    useNotify,
    SaveButton,
    Toolbar,
} from "react-admin";
import { Dialog, DialogTitle, DialogContent, Button } from "@mui/material";
import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import CancelIcon from "@mui/icons-material/Cancel";

import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
} from "../types";
import {
    TextInputWide,
    AutocompleteInputMedium,
} from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ObservationAssessment = () => {
    const [open, setOpen] = React.useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const observationUpdate = async (data: any) => {
        const patch = {
            severity: data.current_severity,
            status: data.current_status,
            comment: data.comment,
        };

        httpClient(
            window.__RUNTIME_CONFIG__.API_BASE_URL +
                "/observations/" +
                data.id +
                "/assessment/",
            {
                method: "PATCH",
                body: JSON.stringify(patch),
            }
        )
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

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

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
            onClick={handleClose}
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
        <React.Fragment>
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
                    <SimpleForm
                        onSubmit={observationUpdate}
                        toolbar={<CustomToolbar />}
                    >
                        <AutocompleteInputMedium
                            source="current_severity"
                            choices={OBSERVATION_SEVERITY_CHOICES}
                            validate={requiredValidate}
                        />
                        <AutocompleteInputMedium
                            source="current_status"
                            choices={OBSERVATION_STATUS_CHOICES}
                            validate={requiredValidate}
                        />
                        <TextInputWide
                            multiline
                            source="comment"
                            validate={requiredValidate}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ObservationAssessment;
