import { Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    ChipField,
    DateField,
    Labeled,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    SortPayload,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { PERMISSION_OBSERVATION_LOG_APPROVAL } from "../../access_control/types";
import MarkdownField from "../../commons/custom_fields/MarkdownField";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { ASSESSMENT_STATUS_NEEDS_APPROVAL } from "../types";
import AssessmentApproval from "./AssessmentApproval";

const ShowActions = () => {
    const observation_log = useRecordContext();

    let filter = null;
    let sort: SortPayload | null = null;
    let storeKey = null;
    if (observation_log && localStorage.getItem("observationlogembeddedlist")) {
        filter = { observation: observation_log.observation };
        sort = { field: "created", order: "DESC" };
        storeKey = "observation_logs.embedded";
    }
    if (observation_log && observation_log.observation_data && localStorage.getItem("observationlogapprovallist")) {
        filter = {
            product: observation_log.observation_data.product,
            assessment_status: ASSESSMENT_STATUS_NEEDS_APPROVAL,
        };
        sort = { field: "created", order: "ASC" };
        storeKey = "observation_logs.approval";
    }

    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {observation_log && filter && sort && storeKey && (
                    <PrevNextButtons filter={filter} linkType="show" sort={sort} storeKey={storeKey} />
                )}
                {observation_log &&
                    observation_log.observation_data &&
                    observation_log.assessment_status == ASSESSMENT_STATUS_NEEDS_APPROVAL &&
                    observation_log.observation_data.product_data.permissions.includes(
                        PERMISSION_OBSERVATION_LOG_APPROVAL
                    ) && <AssessmentApproval observation_log_id={observation_log.id} />}
            </Stack>
        </TopToolbar>
    );
};

const ObservationLogComponent = () => {
    return (
        <WithRecord
            render={(observation_log) => (
                <SimpleShowLayout>
                    <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                        <Stack spacing={1}>
                            <Typography variant="h6">Observation Log</Typography>
                            <Labeled label="Product">
                                <ReferenceField source="observation_data.product" reference="products" link="show">
                                    <TextField source="name" />
                                </ReferenceField>
                            </Labeled>
                            <Labeled label="Observation">
                                <ReferenceField source="observation" reference="observations" link="show">
                                    <TextField source="title" />
                                </ReferenceField>
                            </Labeled>
                            <Labeled label="User">
                                <TextField source="user_full_name" />
                            </Labeled>
                            {observation_log.severity && (
                                <Labeled label="Severity">
                                    <SeverityField source="severity" />
                                </Labeled>
                            )}
                            {observation_log.status && (
                                <Labeled label="Status">
                                    <ChipField
                                        source="status"
                                        sx={{
                                            width: "fit-content",
                                        }}
                                    />
                                </Labeled>
                            )}
                            {observation_log.vex_justification && (
                                <Labeled label="VEX justification">
                                    <TextField source="vex_justification" />
                                </Labeled>
                            )}
                            {observation_log.general_rule != null && (
                                <Labeled label="General rule">
                                    <ReferenceField
                                        source="general_rule"
                                        reference="general_rules"
                                        label="General rule name"
                                        link="show"
                                    />
                                </Labeled>
                            )}
                            {observation_log.product_rule != null && (
                                <Labeled label="Product rule">
                                    <ReferenceField
                                        source="product_rule"
                                        reference="product_rules"
                                        label="Product rule name"
                                        link="show"
                                    />
                                </Labeled>
                            )}
                            <Labeled label="Comment">
                                <MarkdownField content={observation_log.comment} />
                            </Labeled>
                            <Labeled label="Created">
                                <DateField source="created" showTime />
                            </Labeled>
                        </Stack>
                    </Paper>

                    {observation_log &&
                        observation_log.observation_data &&
                        (observation_log.observation_data.product_data.assessments_need_approval ||
                            observation_log.observation_data.product_data.product_group_assessments_need_approval) && (
                            <Paper sx={{ marginBottom: 1, padding: 2, width: "100%" }}>
                                <Stack spacing={1}>
                                    <Typography variant="h6">Approval</Typography>
                                    <Labeled label="Assessment status">
                                        <ChipField
                                            source="assessment_status"
                                            sx={{
                                                width: "fit-content",
                                            }}
                                        />
                                    </Labeled>
                                    {observation_log.approval_user_full_name && (
                                        <Labeled label="Approved/rejected by">
                                            <TextField source="approval_user_full_name" />
                                        </Labeled>
                                    )}
                                    {observation_log.approval_remark && (
                                        <Labeled label="Approval/rejection remark">
                                            <TextField source="approval_remark" />
                                        </Labeled>
                                    )}
                                    {observation_log.approval_date && (
                                        <Labeled label="Approval/rejection date">
                                            <DateField source="approval_date" showTime />
                                        </Labeled>
                                    )}
                                </Stack>
                            </Paper>
                        )}
                </SimpleShowLayout>
            )}
        />
    );
};
const ObservationLogShow = () => {
    return (
        <Show actions={<ShowActions />} component={ObservationLogComponent}>
            <Fragment />
        </Show>
    );
};

export default ObservationLogShow;
