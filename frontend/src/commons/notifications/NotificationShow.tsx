import { Stack, Typography } from "@mui/material";
import {
    DateField,
    DeleteWithConfirmButton,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

const ShowActions = () => {
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "created", order: "DESC" }}
                    storeKey="notifications.list"
                />
                <DeleteWithConfirmButton />
            </Stack>
        </TopToolbar>
    );
};

const NotificationShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(notification) => (
                    <SimpleShowLayout>
                        <Typography variant="h6">Notification</Typography>
                        <TextField source="type" />
                        <TextField source="name" />
                        <DateField source="created" showTime={true} />
                        {notification && notification.message && <TextField source="message" />}
                        {notification && notification.function && <TextField source="function" />}
                        {notification && notification.arguments && <TextField source="arguments" />}
                        {notification && notification.product && (
                            <ReferenceField source="product" reference="products" link="show" />
                        )}
                        {notification && notification.observation && (
                            <ReferenceField source="observation" reference="observations" link="show" />
                        )}
                        <TextField source="user_full_name" label="User" />
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default NotificationShow;
