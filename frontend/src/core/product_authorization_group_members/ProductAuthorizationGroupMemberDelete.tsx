import DeleteIcon from "@mui/icons-material/Delete";
import { useState } from "react";
import { Button, Confirm, useDelete, useNotify, useRefresh } from "react-admin";

type ProductAuthorizationGroupMemberDeleteProps = {
    product_authorization_group_member: any;
};

const ProductAuthorizationGroupMemberDelete = (props: ProductAuthorizationGroupMemberDeleteProps) => {
    const [open, setOpen] = useState(false);
    const [deleteOne] = useDelete();
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        deleteOne(
            "product_authorization_group_members",
            { id: props.product_authorization_group_member.id },
            {
                onSuccess: () => {
                    refresh();
                    notify("Authorization group member deleted", {
                        type: "success",
                    });
                },
                onError: (error: any) => {
                    notify("Authorization group member could not be deleted: " + error.message, {
                        type: "warning",
                    });
                },
            }
        );
        setOpen(false);
    };

    return (
        <>
            <Button label="Delete" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open}
                title="Delete authorization group member"
                content={
                    "Are you sure you want to delete the authorization group member " +
                    props.product_authorization_group_member.authorization_group_name +
                    "?"
                }
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default ProductAuthorizationGroupMemberDelete;
