import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    DateInput,
    FormDataConsumer,
    SaveButton,
    SimpleForm,
    Toolbar,
    useListContext,
    useNotify,
    useRefresh,
    useUnselectAll,
} from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import { validate_after_today, validate_required_4096 } from "../../commons/custom_validators";
import { justificationIsEnabledForStatus, settings_risk_acceptance_expiry_date } from "../../commons/functions";
import { AutocompleteInputMedium, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
    OBSERVATION_STATUS_RISK_ACCEPTED,
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../types";

type ObservationBulkAssessmentButtonProps = {
    product: any;
};

const ObservationBulkAssessment = (props: ObservationBulkAssessmentButtonProps) => {
    const [open, setOpen] = useState(false);
    const [status, setStatus] = useState(OBSERVATION_STATUS_OPEN);
    const justificationEnabled = justificationIsEnabledForStatus(status);
    const refresh = useRefresh();
    const [loading, setLoading] = useState(false);
    const notify = useNotify();
    const { selectedIds } = useListContext();
    const unselectAll = useUnselectAll("observations");

    const observationUpdate = async (data: any) => {
        setLoading(true);
        let url = "";
        if (props.product) {
            url =
                window.__RUNTIME_CONFIG__.API_BASE_URL +
                "/products/" +
                props.product.id +
                "/observations_bulk_assessment/";
        } else {
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/observations/bulk_assessment/";
        }
        const assessment_data = {
            severity: data.current_severity,
            status: data.current_status,
            comment: data.comment,
            vex_justification: justificationEnabled ? data.current_vex_justification : "",
            observations: selectedIds,
            risk_acceptance_expiry_date: data.risk_acceptance_expiry_date,
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

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ padding: "0px" }}
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
                            onChange={(e) => setStatus(e)}
                        />
                        {justificationEnabled && (
                            <AutocompleteInputMedium
                                source="current_vex_justification"
                                label="VEX justification"
                                choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                            />
                        )}
                        <FormDataConsumer>
                            {({ formData }) =>
                                formData.current_status &&
                                formData.current_status == OBSERVATION_STATUS_RISK_ACCEPTED &&
                                (formData.risk_acceptance_expiry_date_calculated ||
                                    settings_risk_acceptance_expiry_date()) && (
                                    <DateInput
                                        source="risk_acceptance_expiry_date"
                                        label="Risk acceptance expiry date"
                                        defaultValue={
                                            formData.risk_acceptance_expiry_date_calculated
                                                ? formData.risk_acceptance_expiry_date_calculated
                                                : settings_risk_acceptance_expiry_date()
                                        }
                                        validate={validate_after_today()}
                                    />
                                )
                            }
                        </FormDataConsumer>
                        <TextInputWide
                            source="comment"
                            validate={validate_required_4096}
                            multiline={true}
                            minRows={3}
                        />
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
