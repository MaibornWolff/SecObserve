import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { CreateBase, SaveButton, SimpleForm, useCreate, useNotify, useRefresh } from "react-admin";

import AddButton from "../../commons/custom_fields/AddButton";
import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { OBSERVATION_STATUS_OPEN } from "../../core/types";
import { RuleCreateEditComponent, non_duplicate_transform, validateRuleForm } from "../functions";

interface CustomToolbarProps {
    handleCancel: () => void;
}

const CustomToolbar = ({ handleCancel }: CustomToolbarProps) => (
    <Toolbar>
        <CancelButton onClick={handleCancel} />
        <SaveButton />
    </Toolbar>
);

export type ProductRuleCreateProps = {
    product: any;
};

const ProductRuleCreate = ({ product }: ProductRuleCreateProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();

    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const create_product_rule = (data: any) => {
        data.product = product.id;
        data = non_duplicate_transform(data);

        create(
            "product_rules",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("Product rule added", { type: "success" });
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
        setOpen(false);
    };

    return (
        <Fragment>
            <AddButton title="Add product rule" onClick={handleOpen} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add product rule</DialogTitle>
                <DialogContent>
                    <CreateBase resource="product_rules">
                        <SimpleForm
                            onSubmit={create_product_rule}
                            toolbar={<CustomToolbar handleCancel={handleCancel} />}
                            validate={validateRuleForm}
                        >
                            <RuleCreateEditComponent product={product} initialStatus={OBSERVATION_STATUS_OPEN} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductRuleCreate;
