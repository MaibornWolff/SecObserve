import { Box, Paper, Stack, Typography } from "@mui/material";
import { Labeled, ReferenceField, TextField, WithRecord } from "react-admin";

const ComponentShowAside = () => {
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
                    <Typography variant="h6" sx={{ marginBottom: 1 }}>
                        Metadata
                    </Typography>
                    <Stack spacing={1}>
                        <Labeled label="Product">
                            <ReferenceField
                                source="product"
                                reference="products"
                                queryOptions={{ meta: { api_resource: "product_names" } }}
                                sx={{ "& a": { textDecoration: "none" } }}
                            />
                        </Labeled>
                        {component.branch_name && (
                            <Labeled label="Branch">
                                <TextField source="branch_name" />
                            </Labeled>
                        )}
                        {component.origin_service_name && (
                            <Labeled label="Service">
                                <TextField source="origin_service_name" />
                            </Labeled>
                        )}
                    </Stack>
                </Paper>
            )}
        />
    );
};

export default ComponentShowAside;
