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

import {
    validate_255,
    validate_513,
    validate_2048,
    validate_required,
    validate_required_255,
} from "../../commons/custom_validators";
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

        if (!data.base_url) {
            data.base_url = "";
        }
        if (!data.project_key) {
            data.project_key = "";
        }
        if (!data.api_key) {
            data.api_key = "";
        }
        if (!data.query) {
            data.query = "";
        }
        if (!data.basic_auth_username) {
            data.basic_auth_username = "";
        }
        if (!data.basic_auth_password) {
            data.basic_auth_password = "";
        }
        if (!data.automatic_import_service) {
            data.automatic_import_service = "";
        }
        if (!data.automatic_import_docker_image_name_tag) {
            data.automatic_import_docker_image_name_tag = "";
        }
        if (!data.automatic_import_endpoint_url) {
            data.automatic_import_endpoint_url = "";
        }
        if (!data.automatic_import_kubernetes_cluster) {
            data.automatic_import_kubernetes_cluster = "";
        }

        create(
            "api_configurations",
            { data: data },
            {
                onSuccess: () => {
                    refresh();
                    notify("API configuration added", { type: "success" });
                    setOpen(false);
                },
                onError: (error: any) => {
                    notify(error.message, { type: "warning" });
                },
            }
        );
    };

    const ParserInput = () => {
        const parserId = useWatch({ name: "parser" });
        const selectedParser = parsers.find((parser) => parser.id === parserId);
        if (selectedParser) {
            switch (selectedParser.name) {
                case "Dependency Track":
                    return (
                        <Fragment>
                            <TextInputWide source="api_key" label="API key" validate={validate_required_255} />
                            <TextInputWide source="project_key" validate={validate_required_255} />
                        </Fragment>
                    );
                case "Trivy Operator Prometheus":
                    return (
                        <Fragment>
                            <TextInputWide source="query" label="Query" validate={validate_required_255} />
                            <BooleanInput
                                source="basic_auth_enabled"
                                label="Basic authentication"
                                defaultValue={false}
                            />
                            <BasicAuthInput />
                        </Fragment>
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
                <Fragment>
                    <TextInputWide source="basic_auth_username" label="Username" validate={validate_required_255} />
                    <PasswordInputWide source="basic_auth_password" label="Password" validate={validate_required_255} />
                </Fragment>
            );
        } else {
            return null;
        }
    };

    const AutomaticImportInput = () => {
        const automatic_import_enabled = useWatch({ name: "automatic_import_enabled" });
        if (automatic_import_enabled) {
            return (
                <Fragment>
                    <ReferenceInput
                        source="automatic_import_branch"
                        reference="branches"
                        sort={{ field: "name", order: "ASC" }}
                        filter={{ product: id }}
                        alwaysOn
                    >
                        <AutocompleteInputWide optionText="name" label="Branch / Version" />
                    </ReferenceInput>
                    <TextInputWide label="Service" source="automatic_import_service" validate={validate_255} />
                    <TextInputWide
                        source="automatic_import_docker_image_name_tag"
                        label="Docker image name:tag"
                        validate={validate_513}
                    />
                    <TextInputWide
                        label="Endpoint URL"
                        source="automatic_import_endpoint_url"
                        validate={validate_2048}
                    />
                    <TextInputWide
                        label="Kubernetes cluster"
                        source="automatic_import_kubernetes_cluster"
                        validate={validate_255}
                    />
                </Fragment>
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
                            <BooleanInput source="automatic_import_enabled" defaultValue={false} />
                            <AutomaticImportInput />
                            <BooleanInput source="test_connection" defaultValue={true} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ApiConfigurationCreate;
