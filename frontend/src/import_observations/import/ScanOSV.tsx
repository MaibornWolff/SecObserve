import UploadIcon from "@mui/icons-material/CloudUpload";
import { Backdrop, Button, CircularProgress, Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { ReferenceInput, SaveButton, SimpleForm, WithRecord, useNotify, useRefresh } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";
import { getIconAndFontColor } from "../../commons/functions";
import { AutocompleteInputWide, TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";

interface ScanOSVProps {
    product: any;
}

const ScanOSV = ({ product }: ScanOSVProps) => {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => {
        setOpen(false);
        setLoading(false);
    };
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
        setLoading(false);
    };

    const scanOSV = async (data: any) => {
        setLoading(true);

        let url = "";
        if (data.branch) {
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/products/" + product.id + "/" + data.branch + "/scan_osv/";
        } else {
            url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/products/" + product.id + "/scan_osv/";
        }

        httpClient(url, {
            method: "POST",
        })
            .then((result) => {
                const message =
                    result.json.observations_new +
                    " new observations\n" +
                    result.json.observations_updated +
                    " updated observations\n" +
                    result.json.observations_resolved +
                    " resolved observations";
                refresh();
                setLoading(false);
                setOpen(false);
                notify(message, {
                    type: "success",
                    multiLine: true,
                });
            })
            .catch((error) => {
                setLoading(false);
                setOpen(false);
                notify(error.message, {
                    type: "warning",
                });
            });
    };

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Scan" icon={<UploadIcon />} alwaysEnable />
        </Toolbar>
    );

    return (
        <Fragment>
            <Button
                onClick={handleOpen}
                size="small"
                sx={{
                    paddingTop: 0,
                    paddingBottom: 0,
                    paddingLeft: "5px",
                    paddingRight: "5px",
                    color: getIconAndFontColor(),
                    textTransform: "none",
                    fontWeight: "normal",
                    fontSize: "1rem",
                }}
                startIcon={<UploadIcon sx={{ color: getIconAndFontColor() }} />}
            >
                Scan vulnerabilities from OSV
            </Button>
            <Dialog open={open && !loading} onClose={handleClose}>
                <DialogTitle>Scan vulnerabilities from OSV</DialogTitle>
                <DialogContent>
                    <SimpleForm onSubmit={scanOSV} toolbar={<CustomToolbar />}>
                        <TextInputWide source="name" defaultValue={product.name} disabled />
                        <WithRecord
                            render={(product) => (
                                <Fragment>
                                    {product.has_branches && (
                                        <ReferenceInput
                                            source="branch"
                                            reference="branches"
                                            sort={{ field: "name", order: "ASC" }}
                                            queryOptions={{ meta: { api_resource: "branch_names" } }}
                                            filter={{ product: product.id }}
                                            alwaysOn
                                        >
                                            <AutocompleteInputWide
                                                optionText="name"
                                                label="Branch / Version"
                                                defaultValue={product.repository_default_branch}
                                            />
                                        </ReferenceInput>
                                    )}
                                </Fragment>
                            )}
                        />
                    </SimpleForm>
                </DialogContent>
            </Dialog>
            {loading ? (
                <Backdrop sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
                    <CircularProgress color="primary" />
                </Backdrop>
            ) : null}
        </Fragment>
    );
};

export default ScanOSV;
