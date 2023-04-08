import { Paper } from "@mui/material";
import {
    ChipField,
    Datagrid,
    FunctionField,
    ListContextProvider,
    Pagination,
    TextField,
    useListController,
} from "react-admin";

import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { humanReadableDate } from "../../commons/functions";
import { OBSERVATION_STATUS_OPEN } from "../types";

const ShowObservations = (id: any) => {
    return "../../../../observations/" + id + "/show";
};

const ObservationDashboardList = () => {
    const filter = {
        age: "Past 7 days",
        current_status: OBSERVATION_STATUS_OPEN,
    };
    const perPage = 10;
    const resource = "observations";
    const sort = { field: "current_severity", order: "ASC" };
    const filterDefaultValues = {};
    const disableSyncWithLocation = true;
    const storeKey = "observations.dashboard";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        filterDefaultValues,
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
                <Paper>
                    <Datagrid size="small" sx={{ width: "100%" }} rowClick={ShowObservations} bulkActionButtons={false}>
                        <TextField source="product_data.name" label="Product" />
                        <TextField source="title" />
                        <SeverityField source="current_severity" />
                        <ChipField source="current_status" label="Status" />
                        <TextField source="scanner_name" label="Scanner" />
                        <FunctionField
                            label="Age"
                            sortBy="last_observation_log"
                            render={(record: { last_observation_log: string }) =>
                                humanReadableDate(record.last_observation_log)
                            }
                        />
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default ObservationDashboardList;
