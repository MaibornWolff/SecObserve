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
} from "react-admin";
import { Paper, Stack } from "@mui/material";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import ApiConfigurationEdit from "./ApiConfigurationEdit";
import APIConfigurationDelete from "./ApiConfigurationDelete";
import {
    PERMISSION_API_CONFIGURATION_EDIT,
    PERMISSION_API_CONFIGURATION_DELETE,
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

type ApiConfigurationEmbeddedListProps = {
    product: any;
};

const ApiConfigurationEmbeddedList = ({
    product,
}: ApiConfigurationEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "api_configurations";
    const sort = { field: "name", order: "ASC" };
    const disableSyncWithLocation = true;
    const storeKey = "api_configurations.embedded";

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
                        <TextField source="base_url" label="Base URL" />
                        <TextField source="project_key" />
                        <WithRecord
                            render={(api_configuration) => (
                                <Stack direction="row" spacing={4}>
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_API_CONFIGURATION_EDIT
                                        ) && <ApiConfigurationEdit />}
                                    {product &&
                                        product.permissions.includes(
                                            PERMISSION_API_CONFIGURATION_DELETE
                                        ) && (
                                            <APIConfigurationDelete
                                                api_configuration={
                                                    api_configuration
                                                }
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

export default ApiConfigurationEmbeddedList;
