import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import * as React from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    required,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { AutocompleteInputWide, PasswordInputWide, SelectInputWide, TextInputWide } from "../../commons/layout/themes";

export type ApiConfigurationCreateProps = {
    id: any;
};

const ApiConfigurationCreate = ({ id }: ApiConfigurationCreateProps) => {
    const [open, setOpen] = React.useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const [create] = useCreate();
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

    const create_api_configuration = (data: any) => {
        data.product = id;
        create(
            "api_configurations",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("API configuration added", { type: "success" });
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
        setOpen(false);
    };

    return (
        <React.Fragment>
            <Button
                variant="contained"
                onClick={handleOpen}
                sx={{ mr: "7px", width: "fit-content", fontSize: "0.8125rem" }}
                startIcon={<AddIcon />}
            >
                Add API configuration
            </Button>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Add API configuration</DialogTitle>
                <DialogContent>
                    <CreateBase resource="api_configurations">
                        <SimpleForm onSubmit={create_api_configuration} toolbar={<CustomToolbar />}>
                            <ReferenceInput
                                source="product"
                                reference="products"
                                sort={{ field: "name", order: "ASC" }}
                            >
                                <SelectInputWide optionText="name" defaultValue={id} disabled={true} />
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
                            <PasswordInputWide source="api_key" label="API key" validate={requiredValidate} />
                            <BooleanInput source="test_connection" defaultValue={true} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    );
};

const requiredValidate = [required()];

export default ApiConfigurationCreate;
