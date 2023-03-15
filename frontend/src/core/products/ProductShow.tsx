import {
    useRecordContext,
    Show,
    SimpleShowLayout,
    TextField,
    EditButton,
    TopToolbar,
    WithRecord,
    TabbedShowLayout,
    Tab,
    BooleanField,
    NumberField,
    Labeled,
    RichTextField,
} from "react-admin";
import { Typography, Stack } from "@mui/material";
import BarChartIcon from "@mui/icons-material/BarChart";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import UploadIcon from "@mui/icons-material/CloudUpload";

import FileUploadObservations from "./FileUploadObservations";
import ApiImportObservations from "./ApiImportObservations";
import ObservationsEmbeddedList from "../observations/ObservationEmbeddedList";
import ProductHeader from "./ProductHeader";
import {
    PERMISSION_PRODUCT_EDIT,
    PERMISSION_PRODUCT_IMPORT_OBSERVATIONS,
    PERMISSION_PRODUCT_MEMBER_CREATE,
    PERMISSION_PRODUCT_RULE_CREATE,
    PERMISSION_API_CONFIGURATION_CREATE,
    PERMISSION_PRODUCT_RULE_APPLY,
    PERMISSION_OBSERVATION_CREATE,
} from "../../access_control/types";
import ProductMemberEmbeddedList from "../product_members/ProductMemberEmbeddedList";
import ProductMemberCreate from "../product_members/ProductMemberCreate";
import MetricSeverities from "../../metrics/MetricSeverities";
import MetricStatus from "../../metrics/MetricStatus";
import ObservationCreate from "../observations/ObservationCreate";
import ProductRuleEmbeddedList from "../../rules/product_rules/ProductRuleEmbeddedList";
import ProductRuleCreate from "../../rules/product_rules/ProductRuleCreate";
import ProductRuleApply from "../../rules/product_rules/ProductRuleApply";
import ApiConfigurationEmbeddedList from "../../import_observations/api_configurations/ApiConfigurationEmbeddedList";
import ApiConfigurationCreate from "../../import_observations/api_configurations/ApiConfigurationCreate";
import ExportMenu from "./ExportMenu";
import products from "../../core/products";
import observations from "../../core/observations";
import general_rules from "../../rules/general_rules";

const ShowActions = () => {
    const product = useRecordContext();
    return (
        <TopToolbar>
            {product &&
                product.permissions.includes(
                    PERMISSION_PRODUCT_IMPORT_OBSERVATIONS
                ) && (
                    <div>
                        <FileUploadObservations />
                        &nbsp; &nbsp;
                        <ApiImportObservations product={product} />
                    </div>
                )}
            <ExportMenu product={product} />
            {product &&
                product.permissions.includes(PERMISSION_PRODUCT_EDIT) && (
                    <EditButton />
                )}
        </TopToolbar>
    );
};

const ProductShow = () => {
    return (
        <div>
            <ProductHeader />
            <Show actions={<ShowActions />}>
                <WithRecord
                    render={(product) => (
                        <TabbedShowLayout>
                            <Tab label="Overview" icon={<products.icon />}>
                                <SimpleShowLayout>
                                    <Typography variant="h6">
                                        Product
                                    </Typography>
                                    <TextField source="name" />
                                    {product.description && (
                                        <RichTextField source="description" />
                                    )}

                                    <Typography
                                        variant="h6"
                                        sx={{ marginTop: "1em" }}
                                    >
                                        Rules
                                    </Typography>
                                    <BooleanField source="apply_general_rules" />

                                    {(product.repository_prefix ||
                                        product.ms_teams_webhook) && (
                                        <Typography
                                            variant="h6"
                                            sx={{ marginTop: "1em" }}
                                        >
                                            Integrations
                                        </Typography>
                                    )}
                                    {product.repository_prefix && (
                                        <TextField source="repository_prefix" />
                                    )}
                                    {product.ms_teams_webhook && (
                                        <TextField
                                            source="ms_teams_webhook"
                                            label="MS Teams Webhook"
                                        />
                                    )}

                                    {product.security_gate_active != null && (
                                        <div>
                                            <Typography
                                                variant="h6"
                                                sx={{ marginTop: "1em" }}
                                            >
                                                Security Gate
                                            </Typography>
                                            <br />
                                            <Labeled>
                                                <BooleanField source="security_gate_active" />
                                            </Labeled>
                                            {product.security_gate_active ==
                                                true && (
                                                <div>
                                                    <Labeled>
                                                        <NumberField source="security_gate_threshold_critical" />
                                                    </Labeled>
                                                    <br />
                                                    <Labeled>
                                                        <NumberField source="security_gate_threshold_high" />
                                                    </Labeled>
                                                    <br />
                                                    <Labeled>
                                                        <NumberField source="security_gate_threshold_medium" />
                                                    </Labeled>
                                                    <br />
                                                    <Labeled>
                                                        <NumberField source="security_gate_threshold_low" />
                                                    </Labeled>
                                                    <br />
                                                    <Labeled>
                                                        <NumberField source="security_gate_threshold_none" />
                                                    </Labeled>
                                                    <br />
                                                    <Labeled>
                                                        <NumberField source="security_gate_unkown" />
                                                    </Labeled>
                                                    <br />
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </SimpleShowLayout>
                            </Tab>
                            <Tab
                                label="Metrics"
                                path="metrics"
                                icon={<BarChartIcon />}
                            >
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                        marginTop: 2,
                                    }}
                                >
                                    <MetricSeverities product_id={product.id} />
                                    <MetricStatus product_id={product.id} />
                                </Stack>{" "}
                            </Tab>
                            <Tab
                                label="Observations"
                                path="observations"
                                icon={<observations.icon />}
                            >
                                {product &&
                                    product.permissions.includes(
                                        PERMISSION_OBSERVATION_CREATE
                                    ) && <ObservationCreate id={product.id} />}
                                <ObservationsEmbeddedList product={product} />
                            </Tab>
                            <Tab
                                label="Rules"
                                path="rules"
                                icon={<general_rules.icon />}
                            >
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                    }}
                                >
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_RULE_CREATE
                                        ) && (
                                            <ProductRuleCreate
                                                id={product.id}
                                            />
                                        )}
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_RULE_APPLY
                                        ) && (
                                            <ProductRuleApply
                                                product={product}
                                            />
                                        )}
                                </Stack>
                                <ProductRuleEmbeddedList product={product} />
                            </Tab>
                            <Tab
                                label="API Configurations"
                                path="api_configurations"
                                icon={<UploadIcon />}
                            >
                                {product &&
                                    product.permissions.includes(
                                        PERMISSION_API_CONFIGURATION_CREATE
                                    ) && (
                                        <ApiConfigurationCreate
                                            id={product.id}
                                        />
                                    )}
                                <ApiConfigurationEmbeddedList
                                    product={product}
                                />
                            </Tab>
                            <Tab
                                label="Members"
                                path="members"
                                icon={<PeopleAltIcon />}
                            >
                                {product &&
                                    product.permissions.includes(
                                        PERMISSION_PRODUCT_MEMBER_CREATE
                                    ) && (
                                        <ProductMemberCreate id={product.id} />
                                    )}
                                <ProductMemberEmbeddedList product={product} />
                            </Tab>
                        </TabbedShowLayout>
                    )}
                />
            </Show>
        </div>
    );
};

export default ProductShow;
