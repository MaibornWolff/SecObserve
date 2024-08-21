import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import { Button, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import {
    BooleanInput,
    ReferenceInput,
    SaveButton,
    SimpleForm,
    Toolbar,
    useDataProvider,
    useNotify,
    useRefresh,
    useUpdate,
} from "react-admin";
import { useWatch } from "react-hook-form";

import { validate_required, validate_required_255 } from "../../commons/custom_validators";
import { AutocompleteInputWide, PasswordInputWide, TextInputWide } from "../../commons/layout/themes";

const ApiConfigurationEdit = () => {
    const [open, setOpen] = useState(false);
    const [parsers, setParsers] = useState<any[]>([]);
    const [update] = useUpdate();
    const refresh = useRefresh();
    const notify = useNotify();
    const dataProvider = useDataProvider();

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

    const api_configuration_update = async (data: any) => {
        const patch = {
            name: data.name,
            parser: data.parser,
            base_url: data.base_url,
            project_key: data.project_key,
            api_key: data.api_key,
            test_connection: data.test_connection,
            query: data.query,
            basic_auth_enabled: data.basic_auth_enabled,
            basic_auth_username: data.basic_auth_username,
            basic_auth_password: data.basic_auth_password,
            verify_ssl: data.verify_ssl,
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
                    <TextInputWide source="basic_auth_username" label="Username" validate={validate_required_255} />
                    <PasswordInputWide source="basic_auth_password" label="Password" validate={validate_required_255} />
                </>
            );
        } else {
            return null;
        }
    };

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
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Edit API configuration</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={api_configuration_update} toolbar={<CustomToolbar />}>
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
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default ApiConfigurationEdit;
