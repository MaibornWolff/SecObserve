import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle, Divider, Typography } from "@mui/material";
import { Fragment, useState } from "react";
import {
    ArrayInput,
    CreateBase,
    FormDataConsumer,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    SimpleFormIterator,
    Toolbar,
    useNotify,
    useRefresh,
} from "react-admin";

import axios_instance from "../../access_control/axios_instance";
import { validate_255, validate_required_200, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";

const OpenVEXCreate = () => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
            }}
            variant="contained"
            onClick={handleCancel}
            color="inherit"
            startIcon={<CancelIcon />}
        >
            Cancel
        </Button>
    );

    const CustomToolbar = () => (
        <Toolbar sx={{ display: "flex", justifyContent: "flex-end" }}>
            <CancelButton />
            <SaveButton label="Create" icon={<AddIcon />} />
        </Toolbar>
    );

    const create_openvex = async (data: any) => {
        data.vulnerability_names = data.vulnerability_names.map((v: any) => v.name);
        data.vulnerability_names = data.vulnerability_names.filter((v: any) => v != null);

        if (data.branch_names) {
            data.branch_names = data.branch_names.map((v: any) => v.name);
            data.branch_names = data.branch_names.filter((v: any) => v != null);
        }

        const url = "vex/openvex_document/create/";
        axios_instance
            .post(url, data, { responseType: "blob" })
            .then(function (response) {
                if (response.status == 204) {
                    notify("No vulnerabilities found to create OpenVEX document", {
                        type: "warning",
                    });
                } else {
                    const blob = new Blob([response.data], { type: "application/json" });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = response.headers["content-disposition"].split("filename=")[1];
                    link.click();

                    refresh();
                    notify("CASF document created", {
                        type: "success",
                    });
                }
            })
            .catch(async function (error) {
                notify(await error.response.data.text(), {
                    type: "warning",
                });
            });

        setOpen(false);
    };

    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<AddIcon />}
            >
                Create OpenVEX document
            </Button>
            <Dialog open={open} onClose={handleClose} maxWidth={"lg"}>
                <DialogTitle>Create OpenVEX document</DialogTitle>
                <DialogContent>
                    <CreateBase resource="openvex">
                        <SimpleForm onSubmit={create_openvex} toolbar={<CustomToolbar />}>
                            <Typography variant="h6">OpenVEX</Typography>
                            <ReferenceInput
                                source="product"
                                reference="products"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <AutocompleteInputWide optionText="name" />
                            </ReferenceInput>
                            <ArrayInput source="vulnerability_names" defaultValue={""} label="Vulnerabilities">
                                <SimpleFormIterator disableReordering inline>
                                    <TextInputWide source="name" validate={validate_255} />
                                </SimpleFormIterator>
                            </ArrayInput>
                            <FormDataConsumer>
                                {({ formData }) =>
                                    formData.product && (
                                        <ArrayInput source="branch_names" defaultValue={""} label="Branches / Versions">
                                            <SimpleFormIterator disableReordering inline>
                                                <TextInputWide source="name" validate={validate_255} />
                                                {/* <ReferenceInput
                                                    source="branch"
                                                    reference="branches"
                                                    sort={{ field: "name", order: "ASC" }}
                                                    filter={{ product: formData.product }}
                                                    alwaysOn
                                                >
                                                    <AutocompleteInputWide optionText="name" label="Name" />
                                                </ReferenceInput> */}
                                            </SimpleFormIterator>
                                        </ArrayInput>
                                    )
                                }
                            </FormDataConsumer>
                            <Divider flexItem sx={{ marginBottom: 2 }} />
                            <Typography variant="h6">Document</Typography>
                            <TextInputWide
                                source="document_id_prefix"
                                label="ID prefix"
                                validate={validate_required_200}
                            />
                            <TextInputWide source="author" validate={validate_required_255} />
                            <TextInputWide source="role" validate={validate_required_255} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default OpenVEXCreate;
