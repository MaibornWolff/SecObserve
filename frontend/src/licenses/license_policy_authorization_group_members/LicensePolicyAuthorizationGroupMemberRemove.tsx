import DeleteIcon from "@mui/icons-material/Delete";
import { useState } from "react";
import { Button, Confirm, useNotify, useRefresh } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";

type LicensePolicyAuthorizationGroupMemberRemoveProps = {
    license_policy_authorization_group_member: any;
};

const LicensePolicyAuthorizationGroupMemberRemove = ({
    license_policy_authorization_group_member,
}: LicensePolicyAuthorizationGroupMemberRemoveProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const removeUser = async () => {
        const url =
            window.__RUNTIME_CONFIG__.API_BASE_URL +
            "/license_policy_authorization_group_members/" +
            license_policy_authorization_group_member.id +
            "/";
        httpClient(url, {
            method: "DELETE",
        })
            .then(() => {
                refresh();
                notify("Authorization group removed", { type: "success" });
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });

        setOpen(false);
    };

    return (
        <>
            <Button label="Remove" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open}
                title="Remove authorization group"
                content={
                    "Are you sure you want to remove the authorization group " +
                    license_policy_authorization_group_member.authorization_group_data.name +
                    "?"
                }
                onConfirm={removeUser}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default LicensePolicyAuthorizationGroupMemberRemove;
