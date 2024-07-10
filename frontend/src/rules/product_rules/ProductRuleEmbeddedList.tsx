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
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { RULE_STATUS_CHOICES } from "../types";

function listFilters(product: any) {
    const filters = [
        <TextInput source="name" alwaysOn />,
        <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }} alwaysOn>
            <AutocompleteInputMedium optionText="name" />
        </ReferenceInput>,
    ];
    if (product && (product.product_rules_need_approval || product.product_group_product_rules_need_approval)) {
        filters.push(
            <AutocompleteInputMedium
                source="approval_status"
                choices={RULE_STATUS_CHOICES}
                label="Approval status"
                alwaysOn
            />
        );
    }
    return filters;
}

type ProductRuleEmbeddedListProps = {
    product: any;
};

const ProductRuleEmbeddedList = ({ product }: ProductRuleEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "product_rules",
        sort: { field: "name", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "product_rules.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    const ShowProductRule = (id: any) => {
        return "../../../../product_rules/" + id + "/show";
    };

    localStorage.setItem("productruleembeddedlist", "true");
    localStorage.removeItem("productruleapprovallist");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters(product)} />
                <Datagrid
                    size={getSettingListSize()}
                    sx={{ width: "100%" }}
                    bulkActionButtons={false}
                    rowClick={ShowProductRule}
                    resource="product_rules"
                >
                    <TextField source="name" />
                    <TextField source="new_severity" />
                    <TextField source="new_status" />
                    {product &&
                        (product.product_rules_need_approval || product.product_group_product_rules_need_approval) && (
                            <ChipField source="approval_status" />
                        )}
                    <BooleanField source="enabled" />
                    <ReferenceField
                        source="parser"
                        reference="parsers"
                        link={false}
                        sx={{ "& a": { textDecoration: "none" } }}
                    />
                    <TextField source="scanner_prefix" />
                    <TextField source="title" label="Observation title" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductRuleEmbeddedList;
