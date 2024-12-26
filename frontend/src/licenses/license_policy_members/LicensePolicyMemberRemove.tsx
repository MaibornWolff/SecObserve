import { useState } from "react";
import { Confirm, useNotify, useRefresh } from "react-admin";

import { httpClient } from "../../commons/ra-data-django-rest-framework";
import RemoveButton from "../../commons/custom_fields/RemoveButton";

type LicensePolicyMemberRemoveProps = {
    license_policy_member: any;
};

const LicensePolicyMemberRemove = ({ license_policy_member }: LicensePolicyMemberRemoveProps) => {
    const [open, setOpen] = useState(false);
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const removeUser = async () => {
        const url =
            window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_policy_members/" + license_policy_member.id + "/";
        httpClient(url, {
            method: "DELETE",
        })
            .then(() => {
                refresh();
                notify("User removed", { type: "success" });
            })
            .catch((error) => {
                notify(error.message, { type: "warning" });
            });

        setOpen(false);
    };

    return (
        <>
            <RemoveButton title="Remove" onClick={handleClick} />
            <Confirm
                isOpen={open}
                title="Remove user"
                content={"Are you sure you want to remove the user " + license_policy_member.user_data.full_name + "?"}
                onConfirm={removeUser}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default LicensePolicyMemberRemove;
