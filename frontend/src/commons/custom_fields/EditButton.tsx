import EditIcon from "@mui/icons-material/Edit";

import SmallButton from "./SmallButton";

interface EditButtonProps {
    title: string;
    onClick: () => void;
    icon?: React.ReactNode;
}

const EditButton = ({ title, onClick, icon }: EditButtonProps) => {
    if (icon === undefined) {
        icon = <EditIcon />;
    }
    return SmallButton({ title, onClick, icon: icon });
};

export default EditButton;
