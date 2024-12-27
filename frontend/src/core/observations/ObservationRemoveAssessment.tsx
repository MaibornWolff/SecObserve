import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, Toolbar, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import RemoveButton from "../../commons/custom_fields/RemoveButton";
import { validate_required_4096 } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ObservationRemoveAssessment = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const observationUpdate = async (data: any) => {
        const patch = {
            comment: data.comment,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/observations/" + data.id + "/remove_assessment/", {
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

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    return (
        <Fragment>
            <RemoveButton title="Remove Assessment" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Observation Remove Assessment</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<CustomToolbar />}>
                        <TextInputWide
                            source="comment"
                            validate={validate_required_4096}
                            multiline={true}
                            minRows={3}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ObservationRemoveAssessment;
