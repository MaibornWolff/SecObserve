import { Stack } from "@mui/material";
import {
    BooleanField,
    ChipField,
    Datagrid,
    FilterForm,
    ListContextProvider,
    ReferenceField,
    ReferenceInput,
    TextField,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";

import {
    PERMISSION_PRODUCT_RULE_APPROVAL,
    PERMISSION_PRODUCT_RULE_DELETE,
    PERMISSION_PRODUCT_RULE_EDIT,
} from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import RuleApproval from "../RuleApproval";
import { RULE_STATUS_NEEDS_APPROVAL } from "../types";
import ProductRuleDelete from "./ProductRuleDelete";
import ProductRuleEdit from "./ProductRuleEdit";

function listFilters() {
    return [
        <TextInput source="name" alwaysOn />,
        <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }} alwaysOn>
            <AutocompleteInputMedium optionText="name" />
        </ReferenceInput>,
    ];
}

type ProductRuleApprovalListProps = {
    product: any;
};

const ProductRuleApprovalList = ({ product }: ProductRuleApprovalListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id), approval_status: RULE_STATUS_NEEDS_APPROVAL },
        perPage: 25,
        resource: "product_rules",
        sort: { field: "name", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "product_rules.approval",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters()} />
                <Datagrid size={getSettingListSize()} sx={{ width: "100%" }} bulkActionButtons={false}>
                    <TextField source="name" />
                    <TextField source="new_severity" />
                    <TextField source="new_status" />
                    {product &&
                        (product.product_rules_need_approval || product.product_group_product_rules_need_approval) && (
                            <ChipField source="approval_status" />
                        )}
                    <BooleanField source="enabled" />
                    <ReferenceField source="parser" reference="parsers" link={false} />
                    <TextField source="scanner_prefix" />
                    <TextField source="title" label="Observation title" />
                    <WithRecord
                        render={(product_rule) => (
                            <Stack direction="row" spacing={4}>
                                {product &&
                                    (product.product_rules_need_approval ||
                                        product.product_group_product_rules_need_approval) &&
                                    product_rule &&
                                    product_rule.approval_status == RULE_STATUS_NEEDS_APPROVAL &&
                                    product_rule.product_data.permissions.includes(
                                        PERMISSION_PRODUCT_RULE_APPROVAL
                                    ) && <RuleApproval rule_id={product_rule.id} class="product_rules" />}
                                {product && product.permissions.includes(PERMISSION_PRODUCT_RULE_EDIT) && (
                                    <ProductRuleEdit />
                                )}
                                {product && product.permissions.includes(PERMISSION_PRODUCT_RULE_DELETE) && (
                                    <ProductRuleDelete product_rule={product_rule} />
                                )}
                            </Stack>
                        )}
                    />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductRuleApprovalList;
