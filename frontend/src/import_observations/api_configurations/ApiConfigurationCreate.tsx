import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useCreate,
    useNotify,
    useRefresh,
} from "react-admin";

import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";

export type ApiConfigurationCreateProps = {
    id: any;
};

const ApiConfigurationCreate = ({ id }: ApiConfigurationCreateProps) => {
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
        <Fragment>
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
                            <TextInputWide autoFocus source="name" validate={validate_required_255} />
                            <ReferenceInput
                                source="parser"
                                reference="parsers"
                                sort={{ field: "name", order: "ASC" }}
                                filter={{ source: "API" }}
                            >
                                <AutocompleteInputWide optionText="name" validate={validate_required} />
                            </ReferenceInput>
                            <TextInputWide source="base_url" label="Base URL" validate={validate_required_255} />
                            <TextInputWide source="project_key" validate={validate_required_255} />
                            <TextInputWide source="api_key" label="API key" validate={validate_required_255} />
                            <BooleanInput source="test_connection" defaultValue={true} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ApiConfigurationCreate;
