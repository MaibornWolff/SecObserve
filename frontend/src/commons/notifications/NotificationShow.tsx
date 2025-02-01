import { Typography } from "@mui/material";
import { useEffect } from "react";
import {
    DateField,
    PrevNextButtons,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
    useGetRecordId,
} from "react-admin";

import { httpClient } from "../ra-data-django-rest-framework";
import { update_notification_count } from "./notification_count";

const ShowActions = () => {
    return (
        <TopToolbar>
            <PrevNextButtons linkType="show" sort={{ field: "created", order: "DESC" }} storeKey="notifications.list" />
        </TopToolbar>
    );
};

const NotificationShow = () => {
    const recordId = useGetRecordId();

    useEffect(() => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/notifications/" + recordId + "/mark_as_read/";
        httpClient(url, {
            method: "POST",
        })
            .then(() => {
                update_notification_count();
            })
            .catch((error) => {
                console.warn("Cannot mark notification as read: ", error.message);
            });
    }, [recordId]);

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
                            <ReferenceField
                                source="product"
                                reference="products"
                                queryOptions={{ meta: { api_resource: "product_names" } }}
                                link="show"
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        )}
                        {notification && notification.observation && (
                            <ReferenceField
                                source="observation"
                                reference="observations"
                                link="show"
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        )}
                        <TextField source="user_full_name" label="User" />
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default NotificationShow;
