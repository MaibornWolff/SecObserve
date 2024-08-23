import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import {
    BooleanInput,
    CreateBase,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useCreate,
    useDataProvider,
    useNotify,
    useRefresh,
} from "react-admin";
import { useWatch } from "react-hook-form";

import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, PasswordInputWide, TextInputWide } from "../../commons/layout/themes";

export type ApiConfigurationCreateProps = {
    id: any;
};

const ApiConfigurationCreate = ({ id }: ApiConfigurationCreateProps) => {
    const [open, setOpen] = useState(false);
    const [parsers, setParsers] = useState<any[]>([]);
    const refresh = useRefresh();
    const notify = useNotify();
    const dataProvider = useDataProvider();
    const [create] = useCreate();

    useEffect(() => {
        // Fetch the list of parsers from the backend
        dataProvider
            .getList("parsers", {
                pagination: { page: 1, perPage: 100 },
                sort: { field: "name", order: "ASC" },
                filter: { source: "API" },
            })
            .then(({ data }) => {
                setParsers(data);
            })
            .catch((error) => {
                notify(`Error fetching parsers: ${error.message}`, { type: "warning" });
            });
    }, [dataProvider, notify]);

    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason === "backdropClick") return;
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

    const createApiConfiguration = (data: any) => {
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

    const ParserInput = () => {
        const parserId = useWatch({ name: "parser" });
        const selectedParser = parsers.find((parser) => parser.id === parserId);
        if (selectedParser) {
            switch (selectedParser.name) {
                case "Dependency Track":
                    return (
                        <>
                            <TextInputWide source="api_key" label="API key" validate={validate_required_255} />
                            <TextInputWide source="project_key" validate={validate_required_255} />
                        </>
                    );
                case "Trivy Operator Prometheus":
                    return (
                        <>
                            <TextInputWide source="query" label="Query" validate={validate_required_255} />
                            <BooleanInput source="basic_auth_enabled" label="Basic Auth" defaultValue={false} />
                            <BasicAuthInput />
                        </>
                    );
            }
        } else {
            return null;
        }
    };

    const BasicAuthInput = () => {
        const basic_auth_enabledId = useWatch({ name: "basic_auth_enabled" });
        if (basic_auth_enabledId) {
            return (
                <>
                    <TextInputWide source="basic_auth_username" validate={validate_required_255} />
                    <PasswordInputWide source="basic_auth_password" validate={validate_required_255} />
                </>
            );
        } else {
            return null;
        }
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
                        <SimpleForm onSubmit={createApiConfiguration} toolbar={<CustomToolbar />}>
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
                            <ParserInput />
                            <BooleanInput source="verify_ssl" label="Verify SSL" defaultValue={true} />
                            <BooleanInput source="test_connection" defaultValue={true} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ApiConfigurationCreate;
