import EditIcon from "@mui/icons-material/Edit";

import SmallButton from "./SmallButton";

interface EditButtonProps {
    title: string;
    onClick: () => void;
}

const EditButton = ({ title, onClick }: EditButtonProps) => {
    return SmallButton({ title, onClick, icon: <EditIcon /> });
};

export default EditButton;
