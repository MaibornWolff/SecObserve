import {
    useListController,
    Datagrid,
    TextField,
    ListContextProvider,
    FilterForm,
    Pagination,
    ReferenceInput,
    TextInput,
    ReferenceField,
    WithRecord,
    BooleanField,
} from "react-admin";
import { Paper, Stack } from "@mui/material";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import ProductRuleEdit from "./ProductRuleEdit";
import ProductRuleDelete from "./ProductRuleDelete";
import {
    PERMISSION_PRODUCT_RULE_EDIT,
    PERMISSION_PRODUCT_RULE_DELETE,
} from "../../access_control/types";

const listFilters = [
    <TextInput source="name" alwaysOn />,
    <ReferenceInput
        source="parser"
        reference="parsers"
        sort={{ field: "name", order: "ASC" }}
        alwaysOn
    >
        <AutocompleteInputMedium optionText="name" />
    </ReferenceInput>,
];

type ProductRuleEmbeddedListProps = {
    product: any;
};

const ProductRuleEmbeddedList = ({ product }: ProductRuleEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "product_rules";
    const sort = { field: "name", order: "ASC" };
    const disableSyncWithLocation = true;
    const storeKey = "product_rules.embedded";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        disableSyncWithLocation,
        storeKey,
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
                <FilterForm filters={listFilters} />
                <Paper>
                    <Datagrid
                        size="medium"
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                    >
                        <TextField source="name" />
                        <ReferenceField
                            source="parser"
                            reference="parsers"
                            link={false}
                        />
                        <TextField source="scanner_prefix" />
                        <TextField source="title" label="Observation title" />
                        <TextField source="new_severity" />
                        <TextField source="new_status" />
                        <BooleanField source="enabled" />
                        <WithRecord
                            render={(product_rule) => (
                                <Stack direction="row" spacing={4}>
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_RULE_EDIT
                                        ) && <ProductRuleEdit />}
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_PRODUCT_RULE_DELETE
                                        ) && (
                                            <ProductRuleDelete
                                                product_rule={product_rule}
                                            />
                                        )}
                                </Stack>
                            )}
                        />
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ProductRuleEmbeddedList;
