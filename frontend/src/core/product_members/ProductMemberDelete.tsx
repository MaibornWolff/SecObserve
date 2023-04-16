import DeleteIcon from "@mui/icons-material/Delete";
import { useState } from "react";
import { Button, Confirm, useDelete, useNotify, useRefresh } from "react-admin";

type ProductMemberDeleteProps = {
    product_member: any;
};

const ProductMemberDelete = (props: ProductMemberDeleteProps) => {
    const [open, setOpen] = useState(false);
    const [deleted, setDeleted] = useState(false);
    const [error_shown, setErrorShown] = useState(false);
    const [deleteOne, { isLoading, error }] = useDelete(); // eslint-disable-line @typescript-eslint/no-unused-vars
    // isLoading is not needed but easier to let it there
    const refresh = useRefresh();
    const notify = useNotify();
    const handleClick = () => setOpen(true);
    const handleDialogClose = () => setOpen(false);

    const handleConfirm = async () => {
        deleteOne("product_members", { id: props.product_member.id });
        setDeleted(true);
        refresh();
        setOpen(false);
    };

    if (error && !error_shown) {
        setErrorShown(true);
        setDeleted(false);
        notify("Product member could not be deleted: " + error, {
            type: "warning",
        });
    } else if (deleted) {
        setDeleted(false);
        notify("Product member deleted");
    }

    return (
        <>
            <Button label="Delete" onClick={handleClick} startIcon={<DeleteIcon />} sx={{ color: "#d32f2f" }} />
            <Confirm
                isOpen={open}
                title="Delete product member"
                content={
                    "Are you sure you want to delete the product member " +
                    props.product_member.user_data.full_name +
                    "?"
                }
                onConfirm={handleConfirm}
                onClose={handleDialogClose}
            />
        </>
    );
};

export default ProductMemberDelete;
