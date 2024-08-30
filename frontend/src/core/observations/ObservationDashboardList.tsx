import { Paper, Typography } from "@mui/material";
import { ChipField, Datagrid, FunctionField, ListContextProvider, TextField, useListController } from "react-admin";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { OBSERVATION_STATUS_OPEN } from "../types";
import { Observation } from "../types";
import ObservationExpand from "./ObservationExpand";
import { IDENTIFIER_OBSERVATION_DASHBOARD_LIST, setListIdentifier } from "./functions";

const ShowObservations = (id: any) => {
    return "../../../../observations/" + id + "/show";
};

const ObservationDashboardList = () => {
    setListIdentifier(IDENTIFIER_OBSERVATION_DASHBOARD_LIST);

    const listContext = useListController({
        filter: {
            age: "Past 7 days",
            current_status: OBSERVATION_STATUS_OPEN,
        },
        perPage: 10,
        resource: "observations",
        sort: { field: "current_severity", order: "ASC" },
        filterDefaultValues: {},
        disableSyncWithLocation: true,
        storeKey: "observations.dashboard",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <Paper sx={{ marginTop: 2, marginBottom: 2, padding: 2 }}>
            <Typography variant="h6" sx={{ paddingBottom: 2 }}>
                Open observations of the last 7 days
            </Typography>
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        rowClick={ShowObservations}
                        bulkActionButtons={false}
                        resource="observations"
                        expand={<ObservationExpand />}
                        expandSingle
                    >
                        <TextField source="product_data.name" label="Product" />
                        <TextField source="title" sx={{ wordBreak: "break-word" }} />
                        <SeverityField label="Severity" source="current_severity" />
                        <ChipField source="current_status" label="Status" />
                        <TextField source="scanner_name" label="Scanner" />
                        <FunctionField<Observation>
                            label="Age"
                            sortBy="last_observation_log"
                            render={(record) => (record ? humanReadableDate(record.last_observation_log) : "")}
                        />
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </Paper>
    );
};

export default ObservationDashboardList;
