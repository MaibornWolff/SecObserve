import { ChipField, Datagrid, DateField, ListContextProvider, TextField, useListController } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { getSettingListSize } from "../../commons/settings/functions";

type ObservationLogEmbeddedListProps = {
    observation: any;
};

const ObservationLogEmbeddedList = ({ observation }: ObservationLogEmbeddedListProps) => {
    const listContext = useListController({
        filter: { observation: Number(observation.id) },
        perPage: 25,
        resource: "observation_logs",
        sort: { field: "created", order: "DESC" },
        disableSyncWithLocation: true,
        storeKey: "observation_logs.embedded",
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

    localStorage.setItem("observationlogembeddedlist", "true");
    localStorage.removeItem("observationlogapprovallist");

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Datagrid
                    size={getSettingListSize()}
                    sx={{ width: "100%" }}
                    bulkActionButtons={false}
                    rowClick={ShowObservationLogs}
                >
                    {(observation.product_data.assessments_need_approval ||
                        observation.product_data.product_group_assessments_need_approval) && (
                        <ChipField source="assessment_status" sortable={false} />
                    )}
                    <TextField source="user_full_name" label="User" sortable={false} />
                    <TextField source="severity" emptyText="---" sortable={false} />
                    <TextField source="status" emptyText="---" sortable={false} />
                    <TextField source="comment" sortable={false} />
                    <DateField source="created" showTime sortable={false} />
                    {(observation.product_data.assessments_need_approval ||
                        observation.product_data.product_group_assessments_need_approval) && (
                        <TextField source="approval_user_full_name" label="Approved/rejected by" sortable={false} />
                    )}
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default ObservationLogEmbeddedList;
