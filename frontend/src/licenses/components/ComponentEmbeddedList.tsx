import {
    AutocompleteInput,
    Datagrid,
    FilterForm,
    ListContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { PURL_TYPE_CHOICES } from "../../core/types";

const showComponent = (id: any) => {
    return "../../../../components/" + id + "/show";
};

const listFilters = [
    <TextInput source="name_version" label="Component" alwaysOn />,
    <AutocompleteInput source="purl_type" label="PURL type" choices={PURL_TYPE_CHOICES} alwaysOn />,
];

type ComponentEmbeddedListProps = {
    component_license: any;
};

const ComponentEmbeddedList = ({ component_license }: ComponentEmbeddedListProps) => {
    const listContext = useListController({
        filter: { component_license: Number(component_license.id) },
        perPage: 25,
        resource: "components",
        sort: { field: "name_version", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "components.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters} />
                <Datagrid
                    size={getSettingListSize()}
                    rowClick={showComponent}
                    bulkActionButtons={false}
                    resource="components"
                >
                    <TextField source="name_version" label="Component" />
                    <TextField source="purl_type" label="PURL type" />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ComponentEmbeddedList;
