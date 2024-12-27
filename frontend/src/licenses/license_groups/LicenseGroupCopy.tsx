import LibraryAddIcon from "@mui/icons-material/LibraryAdd";
import { Dialog, DialogContent, DialogTitle } from "@mui/material";
import { Fragment, useState } from "react";
import { CreateBase, SaveButton, SimpleForm, useNotify, useRefresh } from "react-admin";
import { useNavigate } from "react-router";

import CancelButton from "../../commons/custom_fields/CancelButton";
import SmallButton from "../../commons/custom_fields/SmallButton";
import { validate_required } from "../../commons/custom_validators";
import { TextInputWide } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import Toolbar from "../../commons/custom_fields/Toolbar";

type LicenseGroupCopyProps = {
    license_group: any;
};

const LicenseGroupCopy = ({ license_group }: LicenseGroupCopyProps) => {
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleOpen = () => setOpen(true);
    const handleCancel = () => setOpen(false);
    const handleClose = (event: object, reason: string) => {
        if (reason && reason == "backdropClick") return;
        setOpen(false);
    };

    const CustomToolbar = () => (
        <Toolbar>
            <CancelButton onClick={handleCancel} />
            <SaveButton label="Copy" icon={<LibraryAddIcon />} />
        </Toolbar>
    );

    const copyLicenseGroup = (data: any) => {
        const url = window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_groups/" + license_group.id + "/copy/";
        const body = JSON.stringify({ name: data.new_name });
        httpClient(url, {
            method: "POST",
            body: body,
        })
            .then((response) => {
                refresh();
                notify("License group copied", { type: "success" });
                navigate("/license_groups/" + response.json.id + "/show");
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });
    };

    return (
        <Fragment>
            <SmallButton title="Copy" onClick={handleOpen} icon={<LibraryAddIcon />} />
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Copy license group</DialogTitle>
                <DialogContent>
                    <CreateBase resource="license_group_members">
                        <SimpleForm onSubmit={copyLicenseGroup} toolbar={<CustomToolbar />}>
                            <TextInputWide source="new_name" label="Name" validate={validate_required} />
                        </SimpleForm>
                    </CreateBase>
                </DialogContent>
            </Dialog>
        </Fragment>
    );
};

export default LicenseGroupCopy;
