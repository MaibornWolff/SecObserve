import { Stack, Typography } from "@mui/material";
import { EditButton, NumberField, PrevNextButtons, Show, SimpleShowLayout, TextField, TopToolbar } from "react-admin";

import { is_superuser } from "../../commons/functions";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "document_id_prefix", order: "ASC" }}
                    storeKey="vex_counters.list"
                />
                {is_superuser() && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const VEXCounterShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <SimpleShowLayout>
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    VEX Counter
                </Typography>
                <TextField source="document_id_prefix" label="Document ID prefix" />
                <NumberField source="year" options={{ useGrouping: false }} />
                <TextField source="counter" />
            </SimpleShowLayout>
        </Show>
    );
};

export default VEXCounterShow;
