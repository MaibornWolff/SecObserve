import { Dialog, DialogContent, DialogTitle, Divider, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import AddButton from "../../commons/custom_fields/AddButton";
import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import {
    validate_255,
    validate_513,
    validate_2048,
    validate_required_255,
    validate_required_2048,
} from "../../commons/custom_validators";
import { justificationIsEnabledForStatus } from "../../commons/functions";
import { AutocompleteInputMedium, AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import {
    OBSERVATION_SEVERITY_CHOICES,
    OBSERVATION_STATUS_CHOICES,
    OBSERVATION_STATUS_OPEN,
    OBSERVATION_VEX_JUSTIFICATION_CHOICES,
} from "../../core/types";
import { non_duplicate_transform, validateRuleForm } from "../functions";

export type ProductRuleCreateProps = {
    id: any;
};

const ProductRuleCreate = ({ id }: ProductRuleCreateProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
    const [status, setStatus] = useState(OBSERVATION_STATUS_OPEN);
    const justificationEnabled = justificationIsEnabledForStatus(status);

    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton />
        </Toolbar>
    );

    const create_product_rule = (data: any) => {
        data.product = id;
        data = non_duplicate_transform(data);
        if (!justificationEnabled || !data.new_vex_justification) {
            data.new_vex_justification = "";
        }

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
                            toolbar={<CustomToolbar />}
                            validate={validateRuleForm}
                        >
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Rule
                            </Typography>
                            <TextInputWide autoFocus source="name" validate={validate_required_255} />
                            <TextInputWide
                                source="description"
                                multiline
                                minRows={3}
                                validate={validate_required_2048}
                                helperText="Markdown supported. Description will be copied into the Observation Log."
                            />
                            <AutocompleteInputMedium source="new_severity" choices={OBSERVATION_SEVERITY_CHOICES} />
                            <AutocompleteInputMedium
                                source="new_status"
                                choices={OBSERVATION_STATUS_CHOICES}
                                onChange={(e) => setStatus(e)}
                            />
                            {justificationEnabled && (
                                <AutocompleteInputMedium
                                    source="new_vex_justification"
                                    choices={OBSERVATION_VEX_JUSTIFICATION_CHOICES}
                                />
                            )}
                            <BooleanInput source="enabled" defaultValue={true} />

                            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Observation
                            </Typography>
                            <ReferenceInput source="parser" reference="parsers" sort={{ field: "name", order: "ASC" }}>
                                <AutocompleteInputWide optionText="name" />
                            </ReferenceInput>
                            <TextInputWide source="scanner_prefix" validate={validate_255} />
                            <TextInputWide
                                source="title"
                                label="Title"
                                helperText="Regular expression to match the observation's title"
                                validate={validate_255}
                            />
                            <TextInputWide
                                source="description_observation"
                                label="Description"
                                helperText="Regular expression to match the observation's description"
                                validate={validate_255}
                            />

                            <Divider flexItem sx={{ marginTop: 2, marginBottom: 2 }} />

                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Origins
                            </Typography>
                            <TextInputWide
                                source="origin_component_name_version"
                                label="Component name:version"
                                helperText="Regular expression to match the component name:version"
                                validate={validate_513}
                            />
                            <TextInputWide
                                source="origin_docker_image_name_tag"
                                label="Docker image name:tag"
                                helperText="Regular expression to match the docker image name:tag"
                                validate={validate_513}
                            />
                            <TextInputWide
                                source="origin_endpoint_url"
                                label="Endpoint URL"
                                helperText="Regular expression to match the endpoint URL"
                                validate={validate_2048}
                            />
                            <TextInputWide
                                source="origin_service_name"
                                label="Service name"
                                helperText="Regular expression to match the service name"
                                validate={validate_255}
                            />
                            <TextInputWide
                                source="origin_source_file"
                                label="Source file"
                                helperText="Regular expression to match the source file"
                                validate={validate_255}
                            />
                            <TextInputWide
                                source="origin_cloud_qualified_resource"
                                label="Cloud qualified resource"
                                helperText="Regular expression to match the cloud qualified resource name"
                                validate={validate_255}
                            />
                            <TextInputWide
                                source="origin_kubernetes_qualified_resource"
                                label="Kubernetes qualified resource"
                                helperText="Regular expression to match the Kubernetes qualified resource name"
                                validate={validate_255}
                            />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ProductRuleCreate;
