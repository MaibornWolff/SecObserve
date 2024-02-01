import { Paper } from "@mui/material";
import { Labeled, RecordContextProvider, TextField, useGetOne } from "react-admin";
import { useParams } from "react-router-dom";

import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { useStyles } from "../../commons/layout/themes";
import { Product } from "../types";

const ProductHeader = () => {
    const { id: id } = useParams<any>();
    // function does not work without non-null assertion
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const { data: product } = useGetOne<Product>("products", { id: id! });
    const { classes } = useStyles();

    function get_open_observation_label(product: Product | undefined) {
        if (!product || product.repository_default_branch == null) {
            return "Open observations";
        }
        return "Open observations (" + product.repository_default_branch_name + ")";
    }

    return (
        <RecordContextProvider value={product}>
            <Paper
                sx={{
                    alignItems: "top",
                    display: "flex",
                    justifyContent: "space-between",
                    padding: 2,
                    marginTop: 2,
                }}
            >
                <Labeled label="Product name">
                    <TextField source="name" className={classes.fontBigBold} />
                </Labeled>
                {product && product.security_gate_passed != undefined && (
                    <Labeled>
                        <SecurityGateTextField />
                    </Labeled>
                )}
                <Labeled label={get_open_observation_label(product)}>
                    <ObservationsCountField withLabel={true} />
                </Labeled>
            </Paper>
        </RecordContextProvider>
    );
};

export default ProductHeader;
