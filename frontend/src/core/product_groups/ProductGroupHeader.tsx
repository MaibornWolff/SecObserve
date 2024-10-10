import { Box, Paper, Typography } from "@mui/material";
import { Labeled, RecordContextProvider, TextField, useGetOne } from "react-admin";
import { useParams } from "react-router-dom";

import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { useStyles } from "../../commons/layout/themes";
import { ProductGroup } from "../types";

const ProductGroupHeader = () => {
    const { id: id } = useParams<any>();
    const { data: product_group } = useGetOne<ProductGroup>("product_groups", { id: id });
    const { classes } = useStyles();

    return (
        <RecordContextProvider value={product_group}>
            <Paper
                sx={{
                    padding: 2,
                    marginTop: 2,
                }}
            >
                <Typography variant="h6" sx={{ marginBottom: 1 }}>
                    Product Group
                </Typography>
                <Box
                    sx={{
                        alignItems: "top",
                        display: "flex",
                        justifyContent: "space-between",
                    }}
                >
                    <Labeled label="Product Group name">
                        <TextField source="name" className={classes.fontBigBold} />
                    </Labeled>
                    <Labeled>
                        <ObservationsCountField label="Open observations" withLabel={true} />
                    </Labeled>
                </Box>
            </Paper>
        </RecordContextProvider>
    );
};

export default ProductGroupHeader;
