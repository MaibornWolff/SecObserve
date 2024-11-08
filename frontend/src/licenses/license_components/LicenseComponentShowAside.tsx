import { Box, Paper, Stack, Typography } from "@mui/material";
import { DateField, Labeled, ReferenceField, TextField, WithRecord } from "react-admin";

import TextUrlField from "../../commons/custom_fields/TextUrlField";

const LicenseComponentShowAside = () => {
    return (
        <Box width={"33%"} marginLeft={2}>
            <MetaData />
        </Box>
    );
};

const MetaData = () => {
    return (
        <WithRecord
            render={(component) => (
                <Paper sx={{ marginBottom: 2, padding: 2 }}>
                    <Typography variant="h6">Metadata</Typography>
                    <Stack spacing={1}>
                        <Labeled label="Product">
                            <ReferenceField
                                source="product"
                                reference="products"
                                queryOptions={{ meta: { api_resource: "product_names" } }}
                                link={(record, reference) => `/${reference}/${record.id}/show/licenses`}
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        </Labeled>
                        {component.license_policy_name != "" && (
                            <Labeled label="License policy">
                                <TextUrlField
                                    text={component.license_policy_name}
                                    url={"#/license_policies/" + component.license_policy_id + "/show"}
                                    label="License policy"
                                />
                            </Labeled>
                        )}
                        {component.branch_name && (
                            <Labeled label="Branch">
                                <TextField source="branch_name" />
                            </Labeled>
                        )}
                        {component.upload_filename != "" && (
                            <Labeled label="Upload filename">
                                <TextField source="upload_filename" />
                            </Labeled>
                        )}
                        <Labeled label="Last change">
                            <DateField source="last_change" showTime />
                        </Labeled>
                        <Labeled label="Last seen">
                            <DateField source="import_last_seen" showTime />
                        </Labeled>
                        <Labeled label="Created">
                            <DateField source="created" showTime />
                        </Labeled>
                    </Stack>
                </Paper>
            )}
        />
    );
};

export default LicenseComponentShowAside;
