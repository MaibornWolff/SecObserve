import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, Toolbar, useNotify, useRefresh, useUpdate } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import { validate_255, validate_required } from "../../commons/custom_validators";
import { AutocompleteInputExtraWide, AutocompleteInputMedium, TextInputExtraWide } from "../../commons/layout/themes";
import { EVALUATION_RESULT_CHOICES } from "../types";

export type LicensePolicyItemEditProps = {
    license_policy_id: any;
    license_policy_item_id: any;
};

const LicensePolicyItemEdit = ({ license_policy_id, license_policy_item_id }: LicensePolicyItemEditProps) => {
    const [open, setOpen] = useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const item_update = async (data: any) => {
        if (!data.license_expression) {
            data.license_expression = "";
        }
        if (!data.unknown_license) {
            data.unknown_license = "";
        }
        if (!data.comment) {
            data.comment = "";
        }

        const patch = {
            license_group: data.license_group,
            license: data.license,
            license_expression: data.license_expression,
            unknown_license: data.unknown_license,
            evaluation_result: data.evaluation_result,
            comment: data.comment,
        };

        update(
            "license_policy_items",

            {
                id: license_policy_item_id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("License policy item updated", {
                        type: "success",
                    });
                    setOpen(false);
                },
                onError: (error: any) => {
                    notify(error.message, {
                        type: "warning",
                    });
                },
            }
        );
    };

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );
    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<EditIcon />}
            >
                Edit
            </Button>
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Edit license policy item</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={item_update} toolbar={<CustomToolbar />}>
                        <ReferenceInput
                            source="license_group"
                            reference="license_groups"
                            label="License group"
                            filter={{ exclude_license_policy: license_policy_id }}
                            sort={{ field: "name", order: "ASC" }}
                        >
                            <AutocompleteInputExtraWide optionText="name" />
                        </ReferenceInput>
                        <ReferenceInput
                            source="license"
                            reference="licenses"
                            label="License"
                            filter={{ exclude_license_policy: license_policy_id }}
                            sort={{ field: "spdx_id", order: "ASC" }}
                        >
                            <AutocompleteInputExtraWide optionText="spdx_id_name" />
                        </ReferenceInput>
                        <TextInputExtraWide
                            source="license_expression"
                            label="License expression"
                            validate={validate_255}
                        />
                        <TextInputExtraWide source="unknown_license" label="Unknown license" validate={validate_255} />
                        <AutocompleteInputMedium
                            source="evaluation_result"
                            label="Evaluation result"
                            choices={EVALUATION_RESULT_CHOICES}
                            validate={validate_required}
                        />
                        <TextInputExtraWide source="comment" label="Comment" validate={validate_255} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicensePolicyItemEdit;
