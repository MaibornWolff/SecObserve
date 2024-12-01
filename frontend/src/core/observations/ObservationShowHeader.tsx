import { Paper, Stack, Typography } from "@mui/material";
import {
    ChipField,
    DateField,
    Labeled,
    RecordContextProvider,
    ReferenceField,
    TextField,
    useRecordContext,
} from "react-admin";

import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { useStyles } from "../../commons/layout/themes";
import ObservationShowDescriptionRecommendation from "./ObservationShowDescriptionRecommendation";

type ObservationShowHeaderProps = {
    observation?: any;
};

const ObservationShowHeader = ({ observation }: ObservationShowHeaderProps) => {
    const { classes } = useStyles();

    let in_observation_log = false;
    const observation_record = useRecordContext();
    if (observation) {
        in_observation_log = true;
    } else {
        observation = observation_record;
    }

    return (
        <RecordContextProvider value={observation}>
            {observation && (
                <Paper sx={{ marginBottom: 2, padding: 2 }}>
                    <Typography variant="h6" sx={{ marginBottom: 1 }}>
                        Observation
                    </Typography>
                    {in_observation_log && (
                        <Stack direction="row" spacing={4} sx={{ marginBottom: 2 }}>
                            <Labeled label="Product">
                                <ReferenceField
                                    source="product_data.id"
                                    reference="products"
                                    queryOptions={{ meta: { api_resource: "product_names" } }}
                                    link="show"
                                    sx={{ "& a": { textDecoration: "none" } }}
                                >
                                    <TextField source="name" />
                                </ReferenceField>
                            </Labeled>
                            {observation.branch && (
                                <Labeled label="Branch/ Version">
                                    <TextField source="branch_name" />
                                </Labeled>
                            )}
                        </Stack>
                    )}
                    <Stack direction="row" spacing={4}>
                        <Stack spacing={2}>
                            <Labeled>
                                <SeverityField label="Severity" source="current_severity" />
                            </Labeled>
                            {!in_observation_log &&
                                observation.parser_severity != "" &&
                                (observation.rule_severity != "" || observation.assessment_severity != "") && (
                                    <Labeled>
                                        <TextField source="parser_severity" />
                                    </Labeled>
                                )}
                            {!in_observation_log && observation.rule_severity != "" && (
                                <Labeled>
                                    <TextField source="rule_severity" />
                                </Labeled>
                            )}
                            {!in_observation_log && observation.assessment_severity != "" && (
                                <Labeled>
                                    <TextField source="assessment_severity" />
                                </Labeled>
                            )}
                        </Stack>
                        <Stack spacing={2}>
                            <Labeled>
                                <ChipField source="current_status" label="Status" />
                            </Labeled>
                            {!in_observation_log &&
                                observation.parser_status != "" &&
                                (observation.rule_status != "" ||
                                    observation.assessment_status != "" ||
                                    observation.vex_status != "") && (
                                    <Labeled>
                                        <TextField source="parser_status" />
                                    </Labeled>
                                )}
                            {!in_observation_log && observation.vex_status != "" && (
                                <Labeled label="VEX status">
                                    <TextField source="vex_status" />
                                </Labeled>
                            )}
                            {!in_observation_log && observation.rule_status != "" && (
                                <Labeled>
                                    <TextField source="rule_status" />
                                </Labeled>
                            )}
                            {!in_observation_log && observation.assessment_status != "" && (
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
                        {!in_observation_log && (
                            <Labeled>
                                <TextField source="title" className={classes.fontBigBold} />
                            </Labeled>
                        )}
                        {in_observation_log && (
                            <Labeled label="Title">
                                <ReferenceField
                                    source="id"
                                    reference="observations"
                                    queryOptions={{ meta: { api_resource: "observation_titles" } }}
                                    link="show"
                                    sx={{ "& a": { textDecoration: "none" } }}
                                >
                                    <TextField source="title" />
                                </ReferenceField>
                            </Labeled>
                        )}
                    </Stack>
                    <ObservationShowDescriptionRecommendation />
                </Paper>
            )}
        </RecordContextProvider>
    );
};

export default ObservationShowHeader;
