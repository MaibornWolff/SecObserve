import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    ChipField,
    DateField,
    EditButton,
    Labeled,
    NumberField,
    PrevNextButtons,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import {
    PERMISSION_OBSERVATION_ASSESSMENT,
    PERMISSION_OBSERVATION_EDIT,
    PERMISSION_OBSERVATION_LOG_APPROVAL,
} from "../../access_control/types";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_cwe_url, get_vulnerability_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import AssessmentApproval from "../observation_logs/AssessmentApproval";
import ObservationLogEmbeddedList from "../observation_logs/ObservationLogEmbeddedList";
import { OBSERVATION_STATUS_IN_REVIEW, OBSERVATION_STATUS_OPEN } from "../types";
import ObservationAssessment from "./ObservationAssessment";
import ObservationRemoveAssessment from "./ObservationRemoveAssessment";
import ObservationsShowAside from "./ObservationShowAside";
import ObservationShowDescriptionRecommendation from "./ObservationShowDescriptionRecommendation";
import ObservationShowOrigins from "./ObservationShowOrigins";
import PotentialDuplicatesList from "./PotentialDuplicatesList";
import {
    IDENTIFIER_OBSERVATION_DASHBOARD_LIST,
    IDENTIFIER_OBSERVATION_EMBEDDED_LIST,
    IDENTIFIER_OBSERVATION_LIST,
    IDENTIFIER_OBSERVATION_REVIEW_LIST,
} from "./functions";

const ShowActions = () => {
    const observation = useRecordContext();
    let filter = null;
    let storeKey = null;
    let filterDefaultValues = {};

    if (localStorage.getItem(IDENTIFIER_OBSERVATION_LIST) === "true") {
        filter = {};
        filterDefaultValues = { current_status: OBSERVATION_STATUS_OPEN };
        storeKey = "observations.list";
    } else if (observation && localStorage.getItem(IDENTIFIER_OBSERVATION_EMBEDDED_LIST) === "true") {
        filter = { product: observation.product };
        storeKey = "observations.embedded";
    } else if (localStorage.getItem(IDENTIFIER_OBSERVATION_DASHBOARD_LIST) === "true") {
        filter = {
            age: "Past 7 days",
            current_status: OBSERVATION_STATUS_OPEN,
        };
        storeKey = "observations.dashboard";
    } else if (observation && localStorage.getItem(IDENTIFIER_OBSERVATION_REVIEW_LIST) === "true") {
        filter = { product: observation.product, current_status: OBSERVATION_STATUS_IN_REVIEW };
        storeKey = "observations.review";
    }

    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                {filter && storeKey && (
                    <PrevNextButtons
                        filter={filter}
                        filterDefaultValues={filterDefaultValues}
                        linkType="show"
                        sort={{ field: "current_severity", order: "ASC" }}
                        storeKey={storeKey}
                    />
                )}
                {observation &&
                    observation.product_data.permissions &&
                    observation.product_data.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT) && (
                        <ObservationAssessment />
                    )}
                {observation &&
                    observation.product_data.permissions &&
                    observation.product_data.permissions.includes(PERMISSION_OBSERVATION_ASSESSMENT) &&
                    (observation.assessment_severity || observation.assessment_status) && (
                        <ObservationRemoveAssessment />
                    )}
                {observation &&
                    observation.product_data.permissions &&
                    observation.parser_data.type == "Manual" &&
                    observation.product_data.permissions.includes(PERMISSION_OBSERVATION_EDIT) && <EditButton />}
                {observation &&
                    observation.assessment_needs_approval &&
                    observation.product_data.permissions.includes(PERMISSION_OBSERVATION_LOG_APPROVAL) && (
                        <AssessmentApproval observation_log_id={observation.assessment_needs_approval} />
                    )}
            </Stack>
        </TopToolbar>
    );
};

const ObservationShowComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(observation) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6">Observation</Typography>
                        <Stack direction="row" spacing={4}>
                            <Stack spacing={2}>
                                <Labeled>
                                    <SeverityField source="current_severity" />
                                </Labeled>
                                {observation.parser_severity != "" &&
                                    (observation.rule_severity != "" || observation.assessment_severity != "") && (
                                        <Labeled>
                                            <TextField source="parser_severity" />
                                        </Labeled>
                                    )}
                                {observation.rule_severity != "" && (
                                    <Labeled>
                                        <TextField source="rule_severity" />
                                    </Labeled>
                                )}
                                {observation.assessment_severity != "" && (
                                    <Labeled>
                                        <TextField source="assessment_severity" />
                                    </Labeled>
                                )}
                            </Stack>
                            <Stack spacing={2}>
                                <Labeled>
                                    <ChipField source="current_status" label="Status" />
                                </Labeled>
                                {observation.parser_status != "" &&
                                    (observation.rule_status != "" ||
                                        observation.assessment_status != "" ||
                                        observation.vex_status != "") && (
                                        <Labeled>
                                            <TextField source="parser_status" />
                                        </Labeled>
                                    )}
                                {observation.vex_status != "" && (
                                    <Labeled label="VEX status">
                                        <TextField source="vex_status" />
                                    </Labeled>
                                )}
                                {observation.rule_status != "" && (
                                    <Labeled>
                                        <TextField source="rule_status" />
                                    </Labeled>
                                )}
                                {observation.assessment_status != "" && (
                                    <Labeled>
                                        <TextField source="assessment_status" />
                                    </Labeled>
                                )}
                            </Stack>
                            {observation.found != null && (
                                <Labeled>
                                    <DateField source="found" />
                                </Labeled>
                            )}
                            {observation.risk_acceptance_expiry_date != null && (
                                <Labeled label="Risk acceptance expiry">
                                    <DateField source="risk_acceptance_expiry_date" />
                                </Labeled>
                            )}
                            <Labeled>
                                <TextField source="title" className={classes.fontBigBold} />
                            </Labeled>
                        </Stack>
                        <ObservationShowDescriptionRecommendation />
                    </Paper>

                    {(observation.vulnerability_id != "" ||
                        observation.cvss3_score != null ||
                        observation.cvss3_vector != "" ||
                        observation.cwe != null ||
                        observation.epss_score != null ||
                        observation.epss_percentile != null) && (
                        <Paper sx={{ marginBottom: 2, padding: 2 }}>
                            <Typography variant="h6">Vulnerability</Typography>
                            <Stack direction="row" spacing={4}>
                                {observation.vulnerability_id != "" &&
                                    get_vulnerability_url(observation.vulnerability_id) == null && (
                                        <Labeled>
                                            <TextField source="vulnerability_id" label="Vulnerability ID" />
                                        </Labeled>
                                    )}
                                {observation.vulnerability_id != "" &&
                                    get_vulnerability_url(observation.vulnerability_id) != null && (
                                        <Labeled label="Vulnerability ID">
                                            <TextUrlField
                                                text={observation.vulnerability_id}
                                                url={
                                                    observation.vulnerability_id &&
                                                    get_vulnerability_url(observation.vulnerability_id)
                                                }
                                            />
                                        </Labeled>
                                    )}
                                {observation.cvss3_score != null && (
                                    <Labeled label="CVSS3 score">
                                        <NumberField source="cvss3_score" />
                                    </Labeled>
                                )}
                                {observation.cvss3_vector != "" && (
                                    <Labeled label="CVSS3 vector">
                                        <TextField source="cvss3_vector" />
                                    </Labeled>
                                )}
                                {observation.cwe != null && (
                                    <Labeled label="CWE">
                                        <TextUrlField text={observation.cwe} url={get_cwe_url(observation.cwe)} />
                                    </Labeled>
                                )}
                                {observation.epss_score != null && (
                                    <Labeled label="EPSS score (%)">
                                        <NumberField source="epss_score" />
                                    </Labeled>
                                )}
                                {observation.epss_percentile != null && (
                                    <Labeled label="EPSS percentile (%)">
                                        <NumberField source="epss_percentile" />
                                    </Labeled>
                                )}
                            </Stack>
                        </Paper>
                    )}

                    <ObservationShowOrigins elevated={true} />

                    <Paper sx={{ marginBottom: 2, padding: 2 }}>
                        <Typography variant="h6" sx={{ paddingBottom: 1 }}>
                            Log
                        </Typography>
                        <ObservationLogEmbeddedList observation={observation} />
                    </Paper>

                    {observation && observation.has_potential_duplicates && (
                        <Paper sx={{ marginBottom: 2, paddingTop: 2, paddingLeft: 2, paddingRight: 2 }}>
                            <Typography variant="h6" sx={{ paddingBottom: 1 }}>
                                Potential Duplicates
                            </Typography>
                            <PotentialDuplicatesList observation={observation} />
                        </Paper>
                    )}
                </Box>
            )}
        />
    );
};

const ObservationShow = () => {
    return (
        <Show actions={<ShowActions />} component={ObservationShowComponent} aside={<ObservationsShowAside />}>
            <Fragment />
        </Show>
    );
};

export default ObservationShow;
