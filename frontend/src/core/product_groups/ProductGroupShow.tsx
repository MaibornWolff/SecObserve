import BarChartIcon from "@mui/icons-material/BarChart";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import TokenIcon from "@mui/icons-material/Token";
import { Stack, Typography } from "@mui/material";
import {
    EditButton,
    RichTextField,
    Show,
    SimpleShowLayout,
    Tab,
    TabbedShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import CreateProductApiToken from "../../access_control/product_api_token/ProductApiTokenCreate";
import ProductApiTokenEmbeddedList from "../../access_control/product_api_token/ProductApiTokenEmbeddedList";
import {
    PERMISSION_PRODUCT_API_TOKEN_CREATE,
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
import ProductMemberCreate from "../product_members/ProductMemberCreate";
import ProductMemberEmbeddedList from "../product_members/ProductMemberEmbeddedList";
import product from "../products";
import ProductEmbeddedList from "../products/ProductEmbeddedList";
import ProductGroupHeader from "./ProductGroupHeader";

const ShowActions = () => {
    const product_group = useRecordContext();
    return (
        <TopToolbar>
            {product_group && product_group.permissions.includes(PERMISSION_PRODUCT_GROUP_EDIT) && <EditButton />}
        </TopToolbar>
    );
};

const ProductGroupShow = () => {
    return (
        <div>
            <ProductGroupHeader />
            <Show actions={<ShowActions />}>
                <WithRecord
                    render={(product_group) => (
                        <TabbedShowLayout>
                            <Tab label="Overview" icon={<product_groups.icon />}>
                                <SimpleShowLayout>
                                    <Typography variant="h6">Product Group</Typography>
                                    <TextField source="name" />
                                    {product_group.description && <RichTextField source="description" />}
                                </SimpleShowLayout>
                            </Tab>
                            <Tab label="Products" path="products" icon={<product.icon />}>
                                <ProductEmbeddedList product_group={product_group} />
                            </Tab>
                            <Tab label="Metrics" path="metrics" icon={<BarChartIcon />}>
                                <SimpleShowLayout>
                                    <MetricsHeader repository_default_branch={undefined} />
                                    <Stack
                                        direction="row"
                                        spacing={2}
                                        sx={{
                                            alignItems: "center",
                                            marginTop: 2,
                                        }}
                                    >
                                        <MetricsSeveritiesCurrent product_id={product_group.id} />
                                        <MetricsSeveritiesTimeline product_id={product_group.id} />
                                        <MetricsStatusCurrent product_id={product_group.id} />
                                    </Stack>{" "}
                                </SimpleShowLayout>
                            </Tab>
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
                                {product_group &&
                                    product_group.permissions.includes(PERMISSION_PRODUCT_MEMBER_CREATE) && (
                                        <ProductMemberCreate id={product_group.id} />
                                    )}
                                <ProductMemberEmbeddedList product={product_group} />
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
        </div>
    );
};

export default ProductGroupShow;
