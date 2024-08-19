import BarChartIcon from "@mui/icons-material/BarChart";
import ChecklistIcon from "@mui/icons-material/Checklist";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import TokenIcon from "@mui/icons-material/Token";
import { Badge, Divider, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    EditButton,
    Labeled,
    NumberField,
    PrevNextButtons,
    RichTextField,
    Show,
    Tab,
    TabbedShowLayout,
    TabbedShowLayoutTabs,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import CreateProductApiToken from "../../access_control/product_api_token/ProductApiTokenCreate";
import ProductApiTokenEmbeddedList from "../../access_control/product_api_token/ProductApiTokenEmbeddedList";
import {
    PERMISSION_PRODUCT_API_TOKEN_CREATE,
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_CREATE,
    PERMISSION_PRODUCT_GROUP_EDIT,
    PERMISSION_PRODUCT_MEMBER_CREATE,
    PERMISSION_PRODUCT_RULE_APPLY,
    PERMISSION_PRODUCT_RULE_CREATE,
} from "../../access_control/types";
import product_groups from "../../core/product_groups";
import MetricsHeader from "../../metrics/MetricsHeader";
import MetricsSeveritiesCurrent from "../../metrics/MetricsSeveritiesCurrent";
import MetricsSeveritiesTimeline from "../../metrics/MetricsSeveritiesTimeLine";
import MetricsStatusCurrent from "../../metrics/MetricsStatusCurrent";
import general_rules from "../../rules/general_rules";
import ProductRuleApply from "../../rules/product_rules/ProductRuleApply";
import ProductRuleCreate from "../../rules/product_rules/ProductRuleCreate";
import ProductRuleEmbeddedList from "../../rules/product_rules/ProductRuleEmbeddedList";
import ProductAuthorizationGroupMemberCreate from "../product_authorization_group_members/ProductAuthorizationGroupMemberCreate";
import ProductAuthorizationGroupMemberEmbeddedList from "../product_authorization_group_members/ProductAuthorizationGroupMemberEmbeddedList";
import ProductMemberCreate from "../product_members/ProductMemberCreate";
import ProductMemberEmbeddedList from "../product_members/ProductMemberEmbeddedList";
import product from "../products";
import ExportMenu from "../products/ExportMenu";
import ProductEmbeddedList from "../products/ProductEmbeddedList";
import ProductGroupHeader from "./ProductGroupHeader";
import ProductGroupReviews from "./ProductGroupReviews";

const ShowActions = () => {
    const product_group = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    storeKey="product_groups.list"
                />
                <ExportMenu product={product_group} is_product_group={true} />
                {product_group && product_group.permissions.includes(PERMISSION_PRODUCT_GROUP_EDIT) && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const ProductGroupShow = () => {
    return (
        <Fragment>
            <ProductGroupHeader />
            <Show actions={<ShowActions />}>
                <WithRecord
                    render={(product_group) => (
                        <TabbedShowLayout tabs={<TabbedShowLayoutTabs variant="scrollable" scrollButtons="auto" />}>
                            <Tab label="Overview" icon={<product_groups.icon />}>
                                <Typography variant="h6">Product Group</Typography>
                                <Stack spacing={1}>
                                    <Labeled>
                                        <TextField source="name" />
                                    </Labeled>
                                    {product_group.description && (
                                        <Labeled>
                                            <RichTextField source="description" label="Description" />
                                        </Labeled>
                                    )}
                                </Stack>
                                {product_group.repository_branch_housekeeping_active != null && (
                                    <Fragment>
                                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                        <Typography variant="h6">Housekeeping (for products)</Typography>

                                        <Labeled label="Housekeeping">
                                            <BooleanField
                                                source="repository_branch_housekeeping_active"
                                                valueLabelFalse="Disabled"
                                                valueLabelTrue="Product group specific"
                                            />
                                        </Labeled>
                                        {product_group.repository_branch_housekeeping_active == true && (
                                            <Stack spacing={1}>
                                                <Labeled label="Keep inactive">
                                                    <NumberField source="repository_branch_housekeeping_keep_inactive_days" />
                                                </Labeled>
                                                <Labeled label="Exempt branches / versions">
                                                    <TextField source="repository_branch_housekeeping_exempt_branches" />
                                                </Labeled>
                                            </Stack>
                                        )}
                                    </Fragment>
                                )}
                                {(product_group.notification_email_to ||
                                    product_group.notification_ms_teams_webhook ||
                                    product_group.notification_slack_webhook) && (
                                    <Fragment>
                                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                        <Typography variant="h6">Notifications (for products)</Typography>
                                        <Stack spacing={1}>
                                            {product_group.notification_email_to && (
                                                <Labeled label="Email">
                                                    <TextField source="notification_email_to" />
                                                </Labeled>
                                            )}
                                            {product_group.notification_ms_teams_webhook && (
                                                <Labeled label="MS Teams">
                                                    <TextField source="notification_ms_teams_webhook" />
                                                </Labeled>
                                            )}
                                            {product_group.notification_slack_webhook && (
                                                <Labeled label="Slack">
                                                    <TextField source="notification_slack_webhook" />
                                                </Labeled>
                                            )}
                                        </Stack>
                                    </Fragment>
                                )}
                                {product_group.security_gate_active != null && (
                                    <Fragment>
                                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                        <Typography variant="h6">Security Gate (for products)</Typography>
                                        <Labeled label="Security gate">
                                            <BooleanField
                                                source="security_gate_active"
                                                valueLabelFalse="Disabled"
                                                valueLabelTrue="Product group specific"
                                            />
                                        </Labeled>
                                        {product_group.security_gate_active == true && (
                                            <Stack spacing={1}>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_critical" />
                                                </Labeled>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_high" />
                                                </Labeled>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_medium" />
                                                </Labeled>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_low" />
                                                </Labeled>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_none" />
                                                </Labeled>
                                                <Labeled>
                                                    <NumberField source="security_gate_threshold_unkown" />
                                                </Labeled>
                                            </Stack>
                                        )}
                                    </Fragment>
                                )}

                                <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                <Typography variant="h6">Review</Typography>
                                <Stack spacing={1}>
                                    <Labeled label="Assessments need approval">
                                        <BooleanField source="assessments_need_approval" />
                                    </Labeled>
                                    <Labeled label="Rules need approval">
                                        <BooleanField source="product_rules_need_approval" />
                                    </Labeled>
                                    <Labeled label='Status "In review" for new observations'>
                                        <BooleanField source="new_observations_in_review" />
                                    </Labeled>
                                </Stack>
                                {product_group.risk_acceptance_expiry_active != null && (
                                    <Fragment>
                                        <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                        <Typography variant="h6">Risk acceptance expiry</Typography>

                                        <Labeled label="Risk acceptance expiry">
                                            <BooleanField
                                                source="risk_acceptance_expiry_active"
                                                valueLabelFalse="Disabled"
                                                valueLabelTrue="Product group specific"
                                            />
                                        </Labeled>
                                        {product_group.risk_acceptance_expiry_active == true && (
                                            <Stack spacing={1}>
                                                <Labeled label="Risk acceptance expiry (days)">
                                                    <NumberField source="risk_acceptance_expiry_days" />
                                                </Labeled>
                                            </Stack>
                                        )}
                                    </Fragment>
                                )}
                            </Tab>
                            <Tab label="Products" path="products" icon={<product.icon />}>
                                <ProductEmbeddedList product_group={product_group} />
                            </Tab>
                            <Tab label="Metrics" path="metrics" icon={<BarChartIcon />}>
                                <MetricsHeader repository_default_branch={undefined} />
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                        marginTop: 1,
                                        marginBottom: 1,
                                    }}
                                >
                                    <MetricsSeveritiesCurrent product_id={product_group.id} />
                                    <MetricsSeveritiesTimeline product_id={product_group.id} />
                                    <MetricsStatusCurrent product_id={product_group.id} />
                                </Stack>
                            </Tab>
                            {product_group.product_rule_approvals > 0 && (
                                <Tab
                                    label="Reviews"
                                    path="reviews"
                                    icon={
                                        <Badge badgeContent={product_group.product_rule_approvals} color="secondary">
                                            <ChecklistIcon />
                                        </Badge>
                                    }
                                >
                                    <ProductGroupReviews product_group={product_group} />
                                </Tab>
                            )}
                            <Tab label="Rules" path="rules" icon={<general_rules.icon />}>
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                    }}
                                >
                                    {product_group &&
                                        product_group.permissions.includes(PERMISSION_PRODUCT_RULE_CREATE) && (
                                            <ProductRuleCreate id={product_group.id} />
                                        )}
                                    {product_group &&
                                        product_group.permissions.includes(PERMISSION_PRODUCT_RULE_APPLY) && (
                                            <ProductRuleApply product={product_group} />
                                        )}
                                </Stack>
                                <ProductRuleEmbeddedList product={product_group} />
                            </Tab>
                            <Tab label="Members" path="members" icon={<PeopleAltIcon />}>
                                <Typography variant="h6">User members</Typography>
                                {product_group &&
                                    product_group.permissions.includes(PERMISSION_PRODUCT_MEMBER_CREATE) && (
                                        <ProductMemberCreate id={product_group.id} />
                                    )}
                                <ProductMemberEmbeddedList product={product_group} />

                                <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                <Typography variant="h6">Authorization group members</Typography>
                                {product_group &&
                                    product_group.permissions.includes(
                                        PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_CREATE
                                    ) && <ProductAuthorizationGroupMemberCreate id={product_group.id} />}
                                <ProductAuthorizationGroupMemberEmbeddedList product={product_group} />
                            </Tab>
                            <Tab label="API Token" path="api_token" icon={<TokenIcon />}>
                                {product_group &&
                                    product_group.permissions.includes(PERMISSION_PRODUCT_API_TOKEN_CREATE) && (
                                        <CreateProductApiToken product={product_group} />
                                    )}
                                <ProductApiTokenEmbeddedList product={product_group} />
                            </Tab>
                        </TabbedShowLayout>
                    )}
                />
            </Show>
        </Fragment>
    );
};

export default ProductGroupShow;
