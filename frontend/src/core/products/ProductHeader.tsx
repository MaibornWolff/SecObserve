import {
    RecordContextProvider,
    useGetOne,
    Labeled,
    TextField,
} from "react-admin";
import { Paper } from "@mui/material";
import { useParams } from "react-router-dom";

import { Product } from "../types";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import { SecurityGateTextField } from "../../commons/custom_fields/SecurityGateTextField";
import { useStyles } from "../../commons/layout/themes";

const ProductHeader = () => {
    const { id: id } = useParams<any>();
    // function does not work without non-null assertion
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const { data: product } = useGetOne<Product>("products", { id: id! });
    const { classes } = useStyles();
    return (
        <RecordContextProvider value={product}>
            {" "}
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
                <Labeled>
                    <SecurityGateTextField />
                </Labeled>
                <Labeled>
                    <ObservationsCountField withLabel={true} />
                </Labeled>
            </Paper>
        </RecordContextProvider>
    );
};

export default ProductHeader;
