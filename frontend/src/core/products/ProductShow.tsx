import AccountTreeIcon from "@mui/icons-material/AccountTree";
import BarChartIcon from "@mui/icons-material/BarChart";
import UploadIcon from "@mui/icons-material/CloudUpload";
import ConstructionIcon from "@mui/icons-material/Construction";
import GradingIcon from "@mui/icons-material/Grading";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import SettingsIcon from "@mui/icons-material/Settings";
import TokenIcon from "@mui/icons-material/Token";
import { Stack } from "@mui/material";
import { Fragment } from "react";
import { useState } from "react";
import {
    EditButton,
    PrevNextButtons,
    Show,
    Tab,
    TabbedShowLayout,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import CreateProductApiToken from "../../access_control/product_api_token/ProductApiTokenCreate";
import ProductApiTokenEmbeddedList from "../../access_control/product_api_token/ProductApiTokenEmbeddedList";
import {
    PERMISSION_API_CONFIGURATION_CREATE,
    PERMISSION_BRANCH_CREATE,
    PERMISSION_OBSERVATION_CREATE,
    PERMISSION_PRODUCT_API_TOKEN_CREATE,
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
import ProductMemberCreate from "../product_members/ProductMemberCreate";
import ProductMemberEmbeddedList from "../product_members/ProductMemberEmbeddedList";
import ServiceEmbeddedList from "../services/ServiceEmbeddedList";
import ExportMenu from "./ExportMenu";
import ProductHeader from "./ProductHeader";
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
    function showSettingsTabs() {
        setSettingsTabsShow(true);
    }

    function hideSettingsTabs() {
        setSettingsTabsShow(false);
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
                        <TabbedShowLayout>
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
                                        <ObservationCreate id={product.id} />
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
                            <Tab
                                label="Vulnerability Checks"
                                path="vulnerability_checks"
                                icon={<GradingIcon />}
                                onClick={hideSettingsTabs}
                            >
                                <VulnerabilityCheckEmbeddedList product={product} long_list={true} />
                            </Tab>
                            <Tab label="Branches" path="branches" icon={<AccountTreeIcon />} onClick={hideSettingsTabs}>
                                {product && product.permissions.includes(PERMISSION_BRANCH_CREATE) && (
                                    <BranchCreate id={product.id} />
                                )}
                                <BranchEmbeddedList product={product} />
                            </Tab>
                            <Tab
                                label="Services"
                                path="services"
                                icon={<ConstructionIcon />}
                                onClick={hideSettingsTabs}
                            >
                                <ServiceEmbeddedList product={product} />
                            </Tab>
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
                                    {product && product.permissions.includes(PERMISSION_PRODUCT_MEMBER_CREATE) && (
                                        <ProductMemberCreate id={product.id} />
                                    )}
                                    <ProductMemberEmbeddedList product={product} />
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
