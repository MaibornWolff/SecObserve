import humanizeDuration from "humanize-duration";
import { Fragment } from "react";
import { AutocompleteInput, Datagrid, DateField, FunctionField, List, TextField, TextInput } from "react-admin";

import periodic_tasks from ".";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { PeriodicTaskStatusField } from "../../commons/custom_fields/PeriodicTaskStatusField";
import ListHeader from "../../commons/layout/ListHeader";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { PERIODIC_TASKS_STATUS_CHOICES } from "../types";

const listFilters = [
    <TextInput source="task" alwaysOn />,
    <AutocompleteInput source="status" choices={PERIODIC_TASKS_STATUS_CHOICES} alwaysOn />,
];

const PeriodicTaskList = () => {
    return (
        <Fragment>
            <ListHeader icon={periodic_tasks.icon} title="Periodic Tasks" />
            <List
                perPage={25}
                pagination={<CustomPagination />}
                filters={listFilters}
                sort={{ field: "start_time", order: "DESC" }}
                actions={false}
                disableSyncWithLocation={false}
            >
                <Datagrid size={getSettingListSize()} rowClick={false} bulkActionButtons={false}>
                    <TextField source="task" />
                    <DateField source="start_time" showTime />
                    <FunctionField source="duration" render={(record) => `${humanizeDuration(record.duration)}`} />
                    <PeriodicTaskStatusField label="Status" />
                    <TextField source="message" sortable={false} />
                </Datagrid>
            </List>
        </Fragment>
    );
};

export default PeriodicTaskList;
