import {
    DateField,
    DeleteWithConfirmButton,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
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
            <SimpleShowLayout>
                <TextField source="type" />
                <TextField source="name" />
                <DateField source="created" showTime={true} />
                <TextField source="message" />
                <TextField source="function" />
                <TextField source="arguments" />
                <ReferenceField source="product" reference="products" link="show" />
                <ReferenceField source="observation" reference="observations" link="show" />
                <ReferenceField source="user" reference="users" link={false} />
            </SimpleShowLayout>
        </Show>
    );
};

export default NotificationShow;
