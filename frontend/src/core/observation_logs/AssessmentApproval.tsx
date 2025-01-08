import ApprovalIcon from "@mui/icons-material/Approval";
import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { SaveButton, SimpleForm, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import SmallButton from "../../commons/custom_fields/SmallButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { ASSESSMENT_STATUS_CHOICES } from "../types";

type AssessmentApprovalProps = {
    observation_log_id: string | number;
};

const AssessmentApproval = (props: AssessmentApprovalProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const saveApproval = async (data: any) => {
        const patch = {
            assessment_status: data.assessment_status,
            approval_remark: data.approval_remark,
        };

        httpClient(
            window.__RUNTIME_CONFIG__.API_BASE_URL + "/observation_logs/" + props.observation_log_id + "/approval/",
            {
                method: "PATCH",
                body: JSON.stringify(patch),
            }
        )
            .then(() => {
                refresh();
                notify("Observation Log updated", {
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

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );
    return (
        <Fragment>
            <SmallButton title="Approval" onClick={handleOpen} icon={<ApprovalIcon />} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle sx={{ display: "flex", alignItems: "center" }}>
                    <ApprovalIcon />
                    &nbsp;&nbsp;Assessment approval
                </DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={saveApproval} toolbar={<CustomToolbar />}>
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
        </Fragment>
    );
};

export default AssessmentApproval;
