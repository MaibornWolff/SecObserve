import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import {
    BooleanInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useNotify,
    useRefresh,
    useUpdate,
} from "react-admin";

import { AutocompleteInputWide, SelectInputWide, TextInputWide } from "../../commons/layout/themes";

const ApiConfigurationEdit = () => {
    const [open, setOpen] = React.useState(false);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };
    const api_configuration_update = async (data: any) => {
        const patch = {
            name: data.name,
            parser: data.parser,
            base_url: data.base_url,
            project_key: data.project_key,
            api_key: data.api_key,
            test_connection: data.test_connection,
        };

        update(
            "api_configurations",

            {
                id: data.id,
                data: patch,
            },
            {
                onSuccess: () => {
                    refresh();
                    notify("API configuration updated", {
                        type: "success",
                    });
                },
                onError: (error: any) => {
                    notify(error.message, {
                        type: "warning",
                    });
                },
            }
        );
        setOpen(false);
    };

    const CancelButton = () => (
        <Button
            sx={{
                mr: "1em",
                direction: "row",
                justifyContent: "center",
                alignItems: "center",
                color: "#000000dd",
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
            <SaveButton />
        </Toolbar>
    );
    return (
        <React.Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{ paddingTop: "0px", paddingBottom: "2px" }}
                startIcon={<EditIcon />}
            >
                Edit
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit API configuration</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={api_configuration_update} toolbar={<CustomToolbar />}>
                        <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }}>
                            <SelectInputWide optionText="name" disabled={true} />
                        </ReferenceInput>
                        <TextInputWide autoFocus source="name" validate={requiredValidate} />
                        <ReferenceInput
                            source="parser"
                            reference="parsers"
                            sort={{ field: "name", order: "ASC" }}
                            filter={{ source: "API" }}
                        >
                            <AutocompleteInputWide optionText="name" validate={requiredValidate} />
                        </ReferenceInput>
                        <TextInputWide source="base_url" validate={requiredValidate} label="Base URL" />
                        <TextInputWide source="project_key" validate={requiredValidate} />
                        <TextInputWide source="api_key" label="API key" validate={requiredValidate} />
                        <BooleanInput source="test_connection" defaultValue={true} />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ApiConfigurationEdit;
