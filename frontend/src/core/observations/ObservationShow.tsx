import { Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    ArrayField,
    ChipField,
    Datagrid,
    DateField,
    EditButton,
    Labeled,
    NumberField,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import { PERMISSION_OBSERVATION_ASSESSMENT, PERMISSION_OBSERVATION_EDIT } from "../../access_control/types";
import LabeledTextField from "../../commons/custom_fields/LabeledTextField";
import MarkdownField from "../../commons/custom_fields/MarkdownField";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { get_cwe_url, get_vulnerability_url } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import { OBSERVATION_STATUS_OPEN } from "../types";
import ObservationAssessment from "./ObservationAssessment";
import ObservationRemoveAssessment from "./ObservationRemoveAssessment";
import ObservationsShowAside from "./ObservationShowAside";
import PotentialDuplicatesList from "./PotentialDuplicatesList";

type ShowActionsProps = {
    filter: any;
    storeKey: string;
};

const ShowActions = (props: ShowActionsProps) => {
    const observation = useRecordContext();
    if (observation) {
        localStorage.setItem("observationshow.id", observation.id.toString());
    }
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    filter={props.filter}
                    filterDefaultValues={{ current_status: OBSERVATION_STATUS_OPEN }}
                    linkType="show"
                    sort={{ field: "current_severity", order: "ASC" }}
                    storeKey={props.storeKey}
                />
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
            </Stack>
        </TopToolbar>
    );
};

const ObservationShow = () => {
    const { classes } = useStyles();

    let filter = {};
    let storeKey = "observations.list";
    const product_id = localStorage.getItem("observationembeddedlist.product");
    if (product_id !== null) {
        filter = { product: Number(product_id) };
        storeKey = "observations.embedded";
    } else if (localStorage.getItem("observationdashboardlist") === "true") {
        filter = { age: "Past 7 days", current_status: "Open" };
        storeKey = "observations.dashboard";
    }

    return (
        <Show actions={<ShowActions filter={filter} storeKey={storeKey} />} aside={<ObservationsShowAside />}>
            <WithRecord
                render={(observation) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Observation</Typography>
                        <Stack direction="row" spacing={4}>
                            <Stack spacing={2}>
                                <Labeled>
                                    <SeverityField source="current_severity" />
                                </Labeled>
                                {observation.parser_severity != "" && (
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
                                {observation.parser_status != "" && (
                                    <Labeled>
                                        <TextField source="parser_status" />
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
                            <Labeled>
                                <TextField source="title" className={classes.fontBigBold} />
                            </Labeled>
                        </Stack>
                        {observation.description != "" && (
                            <Labeled label="Description">
                                <MarkdownField content={observation.description} />
                            </Labeled>
                        )}
                        {observation.recommendation != "" && (
                            <Labeled label="Recommendation">
                                <MarkdownField content={observation.recommendation} />
                            </Labeled>
                        )}
                        {(observation.vulnerability_id != "" ||
                            observation.cvss3_score != null ||
                            observation.cvss3_vector != "" ||
                            observation.cwe != null ||
                            observation.epss_score != null ||
                            observation.epss_percentile != null) && (
                            <div>
                                <Typography variant="h6" sx={{ paddingTop: "16px" }}>
                                    Vulnerability
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.vulnerability_id != "" &&
                                        get_vulnerability_url(observation.vulnerability_id) == null && (
                                            <Labeled>
                                                <TextField source="vulnerability_id" label="Vulnerability id" />
                                            </Labeled>
                                        )}
                                    {observation.vulnerability_id != "" &&
                                        get_vulnerability_url(observation.vulnerability_id) != null && (
                                            <Labeled label="Vulnerability id">
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
                                        <Labeled label="CVSS3 Vector">
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
                            </div>
                        )}
                        <Typography variant="h6" sx={{ paddingTop: "16px" }}>
                            Origins
                        </Typography>
                        {observation.origin_service_name != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Service
                                </Typography>
                                <Labeled>
                                    <TextField source="origin_service_name" label="Name" />
                                </Labeled>
                            </div>
                        )}
                        {observation.origin_component_name != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Component
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_component_name != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_name" label="Component name" />
                                        </Labeled>
                                    )}
                                    {observation.origin_component_version != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_version" label="Component version" />
                                        </Labeled>
                                    )}
                                    {observation.origin_component_purl != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_purl" label="Component PURL" />
                                        </Labeled>
                                    )}
                                    {observation.origin_component_cpe != "" && (
                                        <Labeled>
                                            <TextField source="origin_component_cpe" label="Component CPE" />
                                        </Labeled>
                                    )}
                                </Stack>
                                {observation.origin_component_dependencies != "" && (
                                    <Labeled label="First component dependency" sx={{ marginTop: 2 }}>
                                        <LabeledTextField text={observation.origin_component_dependencies} />
                                    </Labeled>
                                )}
                            </div>
                        )}
                        {observation.origin_docker_image_name != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Docker
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_docker_image_name != "" && (
                                        <Labeled>
                                            <TextField source="origin_docker_image_name" label="Docker image name" />
                                        </Labeled>
                                    )}
                                    {observation.origin_docker_image_tag != "" && (
                                        <Labeled>
                                            <TextField source="origin_docker_image_tag" label="Docker image tag" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </div>
                        )}
                        {observation.origin_endpoint_url != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Endpoint
                                </Typography>
                                {observation.origin_endpoint_url != "" && (
                                    <Labeled label="Endpoint URL">
                                        <TextUrlField
                                            text={observation.origin_endpoint_url}
                                            url={observation.origin_endpoint_url}
                                        />
                                    </Labeled>
                                )}
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_endpoint_scheme != "" && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_scheme" label="Endpoint scheme" />
                                        </Labeled>
                                    )}
                                    {observation.origin_endpoint_hostname != "" && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_hostname" label="Endpoint host" />
                                        </Labeled>
                                    )}
                                    {observation.origin_endpoint_port != null && (
                                        <Labeled>
                                            <TextField source="origin_endpoint_port" label="Endpoint port" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </div>
                        )}
                        {observation.origin_source_file != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Source
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_source_file != "" && (
                                        <Labeled>
                                            <TextUrlField
                                                text={observation.origin_source_file}
                                                url={observation.origin_source_file_url}
                                                label="Source file"
                                            />
                                        </Labeled>
                                    )}
                                    {observation.origin_source_line_start != null && (
                                        <Labeled>
                                            <TextField source="origin_source_line_start" label="Source line start" />
                                        </Labeled>
                                    )}
                                    {observation.origin_source_line_end != null && (
                                        <Labeled>
                                            <TextField source="origin_source_line_end" label="Source line end" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </div>
                        )}
                        {observation.origin_cloud_provider != "" && (
                            <div>
                                <Typography variant="subtitle1" sx={{ paddingTop: "8px" }}>
                                    Cloud
                                </Typography>
                                <Stack direction="row" spacing={4}>
                                    {observation.origin_cloud_provider != "" && (
                                        <Labeled>
                                            <TextField source="origin_cloud_provider" label="Provider" />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_account_subscription_project != null && (
                                        <Labeled>
                                            <TextField
                                                source="origin_cloud_account_subscription_project"
                                                label="Account / Subscription / Project"
                                            />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_resource != null && (
                                        <Labeled>
                                            <TextField source="origin_cloud_resource" label="Resource" />
                                        </Labeled>
                                    )}
                                    {observation.origin_cloud_resource_type != null && (
                                        <Labeled>
                                            <TextField source="origin_cloud_resource_type" label="Resource type" />
                                        </Labeled>
                                    )}
                                </Stack>
                            </div>
                        )}
                        <Typography variant="h6" sx={{ paddingTop: "16px" }}>
                            Log
                        </Typography>{" "}
                        <ArrayField label={false} source="observation_logs">
                            <Datagrid bulkActionButtons={false}>
                                <ReferenceField source="user" reference="users">
                                    <TextField source="full_name" />
                                </ReferenceField>
                                <TextField source="severity" emptyText="---" />
                                <TextField source="status" emptyText="---" />
                                <TextField source="comment" />
                                <DateField source="created" showTime />
                            </Datagrid>
                        </ArrayField>
                        {observation && observation.has_potential_duplicates && (
                            <Fragment>
                                <Typography variant="h6" sx={{ paddingTop: "16px", paddingBottom: "8px" }}>
                                    Potential Duplicates
                                </Typography>{" "}
                                <PotentialDuplicatesList observation={observation} />
                            </Fragment>
                        )}
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default ObservationShow;
