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

import { TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ObservationRemoveAssessment = () => {
    const [open, setOpen] = React.useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const observationUpdate = async (data: any) => {
        const patch = {
            comment: data.comment,
        };

        httpClient(
            window.__RUNTIME_CONFIG__.API_BASE_URL +
                "/observations/" +
                data.id +
                "/remove_assessment/",
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
                sx={{
                    paddingTop: "0px",
                    paddingBottom: "2px",
                    color: "#d32f2f",
                }}
                startIcon={<PlaylistAddCheckIcon />}
            >
                Remove Assessment
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Observation Remove Assessment</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={observationUpdate}
                        toolbar={<CustomToolbar />}
                    >
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

export default ObservationRemoveAssessment;
