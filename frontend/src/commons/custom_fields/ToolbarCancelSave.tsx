import { SaveButton } from "react-admin";

import CancelButton from "../../commons/custom_fields/CancelButton";
import Toolbar from "../../commons/custom_fields/Toolbar";

interface ToolbarCancelSaveProps {
    onClick: () => void;
    saveButtonLabel?: string;
    saveButtonIcon?: React.ReactNode;
    alwaysEnable?: boolean;
}

export const ToolbarCancelSave = ({
    onClick,
    saveButtonLabel,
    saveButtonIcon,
    alwaysEnable,
}: ToolbarCancelSaveProps) => (
    <Toolbar>
        <CancelButton onClick={onClick} />
        {saveButtonLabel && !saveButtonIcon && <SaveButton label={saveButtonLabel} />}
        {saveButtonLabel && saveButtonIcon && !alwaysEnable && (
            <SaveButton label={saveButtonLabel} icon={saveButtonIcon} />
        )}
        {saveButtonLabel && saveButtonIcon && alwaysEnable && (
            <SaveButton label={saveButtonLabel} icon={saveButtonIcon} alwaysEnable />
        )}
        {!saveButtonLabel && alwaysEnable && <SaveButton alwaysEnable />}
        {!saveButtonLabel && !alwaysEnable && <SaveButton />}
    </Toolbar>
);
