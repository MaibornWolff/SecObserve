import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SimpleForm, useNotify, useRefresh } from "react-admin";

import RemoveButton from "../../commons/custom_fields/RemoveButton";
import { ToolbarCancelSave } from "../../commons/custom_fields/ToolbarCancelSave";
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

    return (
        <Fragment>
            <RemoveButton title="Remove Assessment" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Observation Remove Assessment</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={observationUpdate} toolbar={<ToolbarCancelSave onClick={handleCancel} />}>
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
