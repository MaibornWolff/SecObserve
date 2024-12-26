import { useState } from "react";
import { Confirm, useDelete, useNotify, useRefresh } from "react-admin";

import RemoveButton from "../../commons/custom_fields/RemoveButton";

type APIConfigurationDeleteProps = {
    api_configuration: any;
};

const APIConfigurationDelete = (props: APIConfigurationDeleteProps) => {
    const [open, setOpen] = useState(false);
    const [deleted, setDeleted] = useState(false);
    const [error_shown, setErrorShown] = useState(false);
    const [deleteOne, { error }] = useDelete();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        deleteOne("api_configurations", { id: props.api_configuration.id });
        setDeleted(true);
        refresh();
        setOpen(false);
    };

    if (error && !error_shown) {
        setErrorShown(true);
        setDeleted(false);
        notify("API configuration could not be deleted: " + error, {
            type: "warning",
        });
    } else if (deleted) {
        setDeleted(false);
        notify("API configuration deleted");
    }

    return (
        <>
            <RemoveButton title="Delete" onClick={handleClick} />
            <Confirm
                isOpen={open}
                title="Delete API configuration"
                content={"Are you sure you want to delete the API configuration " + props.api_configuration.name + "?"}
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default APIConfigurationDelete;
