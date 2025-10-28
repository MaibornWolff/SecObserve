import {
    Datagrid,
    FilterForm,
    ListContextProvider,
    ReferenceField,
    ResourceContextProvider,
    TextField,
    TextInput,
    WithRecord,
    useListController,
} from "react-admin";
import { Fragment } from "react/jsx-runtime";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";

function listFilters() {
    return [<TextInput source="name" id="api_token_name" alwaysOn />];
}

const AccessControlApiTokenEmbeddedList = () => {
    const listContext = useListController({
        filter: {},
        perPage: 25,
        resource: "api_tokens",
        sort: { field: "name", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: false,
        storeKey: "api_tokens.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ResourceContextProvider value="api_tokens">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <FilterForm filters={listFilters()} />
                    <Datagrid
                        size={getSettingListSize()}
                        rowClick={false}
                        bulkActionButtons={false}
                        resource="api_tokens"
                    >
                        <TextField source="name" />
                        <WithRecord
                            label="Product"
                            render={(api_token) => (
                                <Fragment>
                                    {api_token.product && (
                                        <ReferenceField
                                            source="product"
                                            reference="products"
                                            queryOptions={{ meta: { api_resource: "product_names" } }}
                                            link={(record: any, reference: any) =>
                                                `../../${reference}/${record.id}/show/api_token`
                                            }
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        />
                                    )}
                                </Fragment>
                            )}
                        />
                        <WithRecord
                            label="Product Group"
                            render={(api_token) => (
                                <Fragment>
                                    {api_token.product_group && (
                                        <ReferenceField
                                            source="product_group"
                                            reference="product_groups"
                                            queryOptions={{ meta: { api_resource: "product_group_names" } }}
                                            link={(record: any, reference: any) =>
                                                `../../${reference}/${record.id}/show/api_token`
                                            }
                                            sx={{ "& a": { textDecoration: "none" } }}
                                        />
                                    )}
                                </Fragment>
                            )}
                        />
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default AccessControlApiTokenEmbeddedList;
