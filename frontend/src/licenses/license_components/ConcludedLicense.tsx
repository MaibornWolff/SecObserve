import PlaylistAddCheckIcon from "@mui/icons-material/PlaylistAddCheck";
import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useRef, useState } from "react";
import { ReferenceInput, SimpleForm, useNotify, useRefresh } from "react-admin";

import SmallButton from "../../commons/custom_fields/SmallButton";
import { ToolbarCancelSave } from "../../commons/custom_fields/ToolbarCancelSave";
import { validate_255 } from "../../commons/custom_validators";
import { AutocompleteInputExtraWide, TextInputExtraWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

const ConcludedLicense = () => {
    const dialogRef = useRef<HTMLDivElement>(null);
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();

    const concludedLicenseUpdate = async (data: any) => {
        if (!data.concluded_license_expression) {
            data.concluded_license_expression = "";
        }
        if (!data.concluded_non_spdx_license) {
            data.concluded_non_spdx_license = "";
        }

        const patch = {
            concluded_spdx_license: data.concluded_spdx_license,
            concluded_license_expression: data.concluded_license_expression,
            concluded_non_spdx_license: data.concluded_non_spdx_license,
        };

        httpClient(window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_components/" + data.id + "/concluded_license/", {
            method: "PATCH",
            body: JSON.stringify(patch),
        })
            .then(() => {
                refresh();
                notify("Concluded license updated", {
                    type: "success",
                });
                setOpen(false);
            })
            .catch((error) => {
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const handleCancel = () => setOpen(false);
    const handleOpen = () => setOpen(true);

    const validateFields = (values: any) => {
        const errors: any = {};

        // check if only one field is set
        const fields = [
            values.concluded_spdx_license,
            values.concluded_license_expression,
            values.concluded_non_spdx_license,
        ];
        const filledFields = fields.filter(Boolean);
        if (filledFields.length > 1) {
            if (values.concluded_spdx_license) {
                errors.concluded_spdx_license = "Only one field must be set";
            }
            if (values.concluded_license_expression) {
                errors.concluded_license_expression = "Only one field must be set";
            }
            if (values.concluded_non_spdx_license) {
                errors.concluded_non_spdx_license = "Only one field must be set";
            }
        }

        return errors;
    };

    return (
        <Fragment>
            <SmallButton title="Add / edit concluded license" onClick={handleOpen} icon={<PlaylistAddCheckIcon />} />
            <Dialog ref={dialogRef} open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Add / edit concluded license</DialogTitle>
                <DialogContent>
                    <SimpleForm
                        onSubmit={concludedLicenseUpdate}
                        toolbar={<ToolbarCancelSave onClick={handleCancel} />}
                        validate={validateFields}
                    >
                        <ReferenceInput
                            source="concluded_spdx_license"
                            reference="licenses"
                            sort={{ field: "spdx_id", order: "ASC" }}
                        >
                            <AutocompleteInputExtraWide label="Concluded SPDX License" optionText="spdx_id_name" />
                        </ReferenceInput>
                        <TextInputExtraWide
                            source="concluded_license_expression"
                            label="Concluded license expression"
                            validate={validate_255}
                        />
                        <TextInputExtraWide
                            source="concluded_non_spdx_license"
                            label="Concluded Non-SPDX license"
                            validate={validate_255}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ConcludedLicense;
