import {
    DateField,
    DeleteWithConfirmButton,
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
            <DeleteWithConfirmButton />
        </TopToolbar>
    );
};

const NotificationShow = () => {
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(notification) => (
                    <SimpleShowLayout>
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
                        {notification && notification.user && (
                            <ReferenceField source="user" reference="users" link={false} />
                        )}
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default NotificationShow;
