import {
    BooleanField,
    EditButton,
    ReferenceField,
    Show,
    SimpleShowLayout,
    TextField,
    TopToolbar,
    WithRecord,
} from "react-admin";

import { useStyles } from "../../commons/layout/themes";

const ShowActions = () => {
    const user = localStorage.getItem("user");
    return <TopToolbar>{user && JSON.parse(user).is_superuser && <EditButton />}</TopToolbar>;
};

const GeneralRuleShow = () => {
    const { classes } = useStyles();
    return (
        <Show actions={<ShowActions />}>
            <WithRecord
                render={(rule) => (
                    <SimpleShowLayout>
                        <TextField source="name" className={classes.fontBigBold} />
                        {rule.description && <TextField source="description" />}
                        {rule.product && <ReferenceField source="product" reference="products" link="show" />}
                        <ReferenceField source="parser" reference="parsers" link="show" />
                        {rule.scanner_prefix && <TextField source="scanner_prefix" />}
                        {rule.title && <TextField source="title" label="Observation title" />}
                        {rule.origin_component_name_version && (
                            <TextField source="origin_component_name_version" label="Origin component name:version" />
                        )}
                        {rule.origin_docker_image_name_tag && (
                            <TextField source="origin_docker_image_name_tag" label="Origin docker image name:tag" />
                        )}
                        {rule.origin_endpoint_url && (
                            <TextField source="origin_endpoint_url" label="Origin endpoint URL" />
                        )}
                        {rule.origin_service_name && (
                            <TextField source="origin_service_name" label="Origin service name" />
                        )}
                        {rule.origin_source_file && (
                            <TextField source="origin_source_file" label="Origin source file" />
                        )}

                        {rule.new_severity && <TextField source="new_severity" />}
                        {rule.new_status && <TextField source="new_status" />}
                        <BooleanField source="enabled" />
                    </SimpleShowLayout>
                )}
            />
        </Show>
    );
};

export default GeneralRuleShow;
