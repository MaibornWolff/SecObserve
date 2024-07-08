import AccountTreeIcon from "@mui/icons-material/AccountTree";
import BarChartIcon from "@mui/icons-material/BarChart";
import ChecklistIcon from "@mui/icons-material/Checklist";
import UploadIcon from "@mui/icons-material/CloudUpload";
import ConstructionIcon from "@mui/icons-material/Construction";
import GradingIcon from "@mui/icons-material/Grading";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import SettingsIcon from "@mui/icons-material/Settings";
import TokenIcon from "@mui/icons-material/Token";
import { Badge, Divider, Stack, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    EditButton,
    PrevNextButtons,
    Show,
    Tab,
    TabbedShowLayout,
    TabbedShowLayoutTabs,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";
import { useLocation } from "react-router";

import CreateProductApiToken from "../../access_control/product_api_token/ProductApiTokenCreate";
import ProductApiTokenEmbeddedList from "../../access_control/product_api_token/ProductApiTokenEmbeddedList";
import {
    PERMISSION_API_CONFIGURATION_CREATE,
    PERMISSION_BRANCH_CREATE,
    PERMISSION_OBSERVATION_CREATE,
    PERMISSION_PRODUCT_API_TOKEN_CREATE,
    PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_CREATE,
    PERMISSION_PRODUCT_EDIT,
    PERMISSION_PRODUCT_IMPORT_OBSERVATIONS,
    PERMISSION_PRODUCT_MEMBER_CREATE,
    PERMISSION_PRODUCT_RULE_APPLY,
    PERMISSION_PRODUCT_RULE_CREATE,
} from "../../access_control/types";
import observations from "../../core/observations";
import ApiConfigurationCreate from "../../import_observations/api_configurations/ApiConfigurationCreate";
import ApiConfigurationEmbeddedList from "../../import_observations/api_configurations/ApiConfigurationEmbeddedList";
import ImportMenu from "../../import_observations/import/ImportMenu";
import VulnerabilityCheckEmbeddedList from "../../import_observations/vulnerability_checks/VulnerabilityCheckEmbeddedList";
import MetricsHeader from "../../metrics/MetricsHeader";
import MetricsSeveritiesCurrent from "../../metrics/MetricsSeveritiesCurrent";
import MetricsSeveritiesTimeline from "../../metrics/MetricsSeveritiesTimeLine";
import MetricsStatusCurrent from "../../metrics/MetricsStatusCurrent";
import general_rules from "../../rules/general_rules";
import ProductRuleApply from "../../rules/product_rules/ProductRuleApply";
import ProductRuleCreate from "../../rules/product_rules/ProductRuleCreate";
import ProductRuleEmbeddedList from "../../rules/product_rules/ProductRuleEmbeddedList";
import BranchCreate from "../branches/BranchCreate";
import BranchEmbeddedList from "../branches/BranchEmbeddedList";
import ShowDefaultBranchObservationsButton from "../branches/ShowDefaultBranchObservationsButton";
import ObservationCreate from "../observations/ObservationCreate";
import ObservationsEmbeddedList from "../observations/ObservationEmbeddedList";
import ProductAuthorizationGroupMemberCreate from "../product_authorization_group_members/ProductAuthorizationGroupMemberCreate";
import ProductAuthorizationGroupMemberEmbeddedList from "../product_authorization_group_members/ProductAuthorizationGroupMemberEmbeddedList";
import ProductMemberCreate from "../product_members/ProductMemberCreate";
import ProductMemberEmbeddedList from "../product_members/ProductMemberEmbeddedList";
import ServiceEmbeddedList from "../services/ServiceEmbeddedList";
import ExportMenu from "./ExportMenu";
import ProductHeader from "./ProductHeader";
import ProductReviews from "./ProductReviews";
import ProductShowProduct from "./ProductShowProduct";

type ShowActionsProps = {
    filter: any;
    storeKey: string;
};

const ShowActions = (props: ShowActionsProps) => {
    const product = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    filter={props.filter}
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    storeKey={props.storeKey}
                />
                {product && product.permissions.includes(PERMISSION_PRODUCT_IMPORT_OBSERVATIONS) && (
                    <ImportMenu product={product} />
                )}
                <ExportMenu product={product} is_product_group={false} />
                {product && product.permissions.includes(PERMISSION_PRODUCT_EDIT) && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const ProductShow = () => {
    const [settingsTabsShow, setSettingsTabsShow] = useState(false);
    const [tabs_changed, setTabsChanged] = useState(false);
    function showSettingsTabs() {
        setSettingsTabsShow(true);
        setTabsChanged(true);
    }

    function hideSettingsTabs() {
        setSettingsTabsShow(false);
        setTabsChanged(true);
    }

    const location = useLocation();
    if (!tabs_changed) {
        setTabsChanged(true);
        setSettingsTabsShow(
            location.pathname.endsWith("api_token") ||
                location.pathname.endsWith("members") ||
                location.pathname.endsWith("rules") ||
                location.pathname.endsWith("api_configurations")
        );
    }
    const settingsLabel = settingsTabsShow ? "Settings" : "Settings >>>";

    let filter = {};
    let storeKey = "products.list";

    const product_group_id = localStorage.getItem("productembeddedlist.product_group");
    if (product_group_id !== null) {
        filter = { product_group: Number(product_group_id) };
        storeKey = "products.embedded";
    }

    return (
        <Fragment>
            <ProductHeader />
            <Show actions={<ShowActions filter={filter} storeKey={storeKey} />}>
                <WithRecord
                    render={(product) => (
                        <TabbedShowLayout tabs={<TabbedShowLayoutTabs variant="scrollable" scrollButtons="auto" />}>
                            <Tab label="Observations" icon={<observations.icon />} onClick={hideSettingsTabs}>
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                    }}
                                >
                                    <ShowDefaultBranchObservationsButton product={product} />
                                    {product && product.permissions.includes(PERMISSION_OBSERVATION_CREATE) && (
                                        <ObservationCreate
                                            id={product.id}
                                            risk_acceptance_expiry_date_calculated={
                                                product.risk_acceptance_expiry_date_calculated
                                            }
                                        />
                                    )}
                                </Stack>
                                <ObservationsEmbeddedList product={product} />
                            </Tab>
                            <Tab label="Metrics" path="metrics" icon={<BarChartIcon />} onClick={hideSettingsTabs}>
                                <MetricsHeader repository_default_branch={product.repository_default_branch_name} />
                                <Stack
                                    direction="row"
                                    spacing={2}
                                    sx={{
                                        alignItems: "center",
                                        marginTop: 1,
                                        marginBottom: 1,
                                    }}
                                >
                                    <MetricsSeveritiesCurrent product_id={product.id} />
                                    <MetricsSeveritiesTimeline product_id={product.id} />
                                    <MetricsStatusCurrent product_id={product.id} />
                                </Stack>
                            </Tab>
                            {product.observation_reviews +
                                product.observation_log_approvals +
                                product.product_rule_approvals >
                                0 && (
                                <Tab
                                    label="Reviews"
                                    path="reviews"
                                    icon={
                                        <Badge
                                            badgeContent={
                                                product.observation_reviews +
                                                product.observation_log_approvals +
                                                product.product_rule_approvals
                                            }
                                            color="secondary"
                                        >
                                            <ChecklistIcon />
                                        </Badge>
                                    }
                                    onClick={hideSettingsTabs}
                                >
                                    <ProductReviews product={product} />
                                </Tab>
                            )}
                            <Tab
                                label="Vulnerability Checks"
                                path="vulnerability_checks"
                                icon={<GradingIcon />}
                                onClick={hideSettingsTabs}
                            >
                                <VulnerabilityCheckEmbeddedList product={product} long_list={true} />
                            </Tab>
                            <Tab
                                label="Branches / Versions"
                                path="branches"
                                icon={<AccountTreeIcon />}
                                onClick={hideSettingsTabs}
                            >
                                {product && product.permissions.includes(PERMISSION_BRANCH_CREATE) && (
                                    <BranchCreate id={product.id} />
                                )}
                                <BranchEmbeddedList product={product} />
                            </Tab>
                            {product.has_services && (
                                <Tab
                                    label="Services"
                                    path="services"
                                    icon={<ConstructionIcon />}
                                    onClick={hideSettingsTabs}
                                >
                                    <ServiceEmbeddedList product={product} />
                                </Tab>
                            )}
                            <Tab
                                label={settingsLabel}
                                path="settings"
                                icon={<SettingsIcon />}
                                onClick={showSettingsTabs}
                            >
                                <ProductShowProduct product={product} />
                            </Tab>
                            {settingsTabsShow && (
                                <Tab label="Rules" path="rules" icon={<general_rules.icon />}>
                                    <Stack
                                        direction="row"
                                        spacing={2}
                                        sx={{
                                            alignItems: "center",
                                        }}
                                    >
                                        {product && product.permissions.includes(PERMISSION_PRODUCT_RULE_CREATE) && (
                                            <ProductRuleCreate id={product.id} />
                                        )}
                                        {product && product.permissions.includes(PERMISSION_PRODUCT_RULE_APPLY) && (
                                            <ProductRuleApply product={product} />
                                        )}
                                    </Stack>
                                    <ProductRuleEmbeddedList product={product} />
                                </Tab>
                            )}
                            {settingsTabsShow && (
                                <Tab label="API Configurations" path="api_configurations" icon={<UploadIcon />}>
                                    {product && product.permissions.includes(PERMISSION_API_CONFIGURATION_CREATE) && (
                                        <ApiConfigurationCreate id={product.id} />
                                    )}
                                    <ApiConfigurationEmbeddedList product={product} />
                                </Tab>
                            )}
                            {settingsTabsShow && (
                                <Tab label="Members" path="members" icon={<PeopleAltIcon />}>
                                    <Typography variant="h6">User members</Typography>
                                    {product && product.permissions.includes(PERMISSION_PRODUCT_MEMBER_CREATE) && (
                                        <ProductMemberCreate id={product.id} />
                                    )}
                                    <ProductMemberEmbeddedList product={product} />

                                    <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                                    <Typography variant="h6">Authorization group members</Typography>
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_AUTHORIZATION_GROUP_MEMBER_CREATE
                                        ) && <ProductAuthorizationGroupMemberCreate id={product.id} />}
                                    <ProductAuthorizationGroupMemberEmbeddedList product={product} />
                                </Tab>
                            )}
                            {settingsTabsShow && (
                                <Tab label="API Token" path="api_token" icon={<TokenIcon />}>
                                    {product && product.permissions.includes(PERMISSION_PRODUCT_API_TOKEN_CREATE) && (
                                        <CreateProductApiToken product={product} />
                                    )}
                                    <ProductApiTokenEmbeddedList product={product} />
                                </Tab>
                            )}
                        </TabbedShowLayout>
                    )}
                />
            </Show>
        </Fragment>
    );
};

export default ProductShow;
