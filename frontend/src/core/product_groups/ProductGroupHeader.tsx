import { Paper } from "@mui/material";
import { Labeled, RecordContextProvider, TextField, useGetOne } from "react-admin";
import { useParams } from "react-router-dom";

import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { useStyles } from "../../commons/layout/themes";
import { ProductGroup } from "../types";

const ProductGroupHeader = () => {
    const { id: id } = useParams<any>();
    // function does not work without non-null assertion
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const { data: product_group } = useGetOne<ProductGroup>("product_groups", { id: id! });
    const { classes } = useStyles();

    return (
        <RecordContextProvider value={product_group}>
            <Paper
                sx={{
                    alignItems: "top",
                    display: "flex",
                    justifyContent: "space-between",
                    padding: 2,
                    marginTop: 2,
                }}
            >
                <Labeled label="Product Group name">
                    <TextField source="name" className={classes.fontBigBold} />
                </Labeled>
                <Labeled label="Open observations">
                    <ObservationsCountField withLabel={true} />
                </Labeled>
            </Paper>
        </RecordContextProvider>
    );
};

export default ProductGroupHeader;
