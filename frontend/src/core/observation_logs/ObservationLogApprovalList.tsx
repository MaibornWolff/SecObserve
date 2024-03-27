import {
    AutocompleteInput,
    ChipField,
    Datagrid,
    DateField,
    FilterForm,
    ListContextProvider,
    ReferenceField,
    ReferenceInput,
    TextField,
    TextInput,
    useListController,
} from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { feature_vex_enabled } from "../../commons/functions";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/settings/functions";
import { ASSESSMENT_STATUS_NEEDS_APPROVAL } from "../types";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";

function listFilters() {
    return [
        <TextInput source="observation_title" label="Observation title" alwaysOn />,
        <ReferenceInput source="user" reference="users" sort={{ field: "full_name", order: "ASC" }} alwaysOn>
            <AutocompleteInputMedium optionText="full_name" />
        </ReferenceInput>,
        <AutocompleteInput source="severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
        <AutocompleteInput source="status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
    ];
}

type ObservationLogApprovalListProps = {
    product: any;
};

const ObservationLogApprovalList = ({ product }: ObservationLogApprovalListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id), assessment_status: ASSESSMENT_STATUS_NEEDS_APPROVAL },
        perPage: 25,
        resource: "observation_logs",
        sort: { field: "created", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "observation_logs.approval",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    const ShowObservationLogs = (id: any) => {
        return "../../../../observation_logs/" + id + "/show";
    };

    localStorage.setItem("observationlogapprovallist", "true");
    localStorage.removeItem("observationlogembeddedlist");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <FilterForm filters={listFilters()} />
                <Datagrid
                    size={getSettingListSize()}
                    sx={{ width: "100%" }}
                    bulkActionButtons={false}
                    rowClick={ShowObservationLogs}
                >
                    <ChipField source="assessment_status" sortable={false} />
                    <ReferenceField source="observation" reference="observations" link="show">
                        <TextField source="title" />
                    </ReferenceField>
                    <TextField source="user_full_name" label="User" />
                    <TextField source="severity" emptyText="---" />
                    <TextField source="status" emptyText="---" />
                    {feature_vex_enabled() && (
                        <TextField label="VEX justification" source="vex_justification" emptyText="---" />
                    )}
                    <TextField source="comment" />
                    <DateField source="created" showTime />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ObservationLogApprovalList;
