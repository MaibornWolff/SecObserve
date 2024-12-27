import { Stack } from "@mui/material";
import { ReactNode } from "react";

interface ToolbarProps {
    children?: ReactNode;
}

const Toolbar = (props: ToolbarProps) => {
    const { children } = props;

    return (
        <Stack direction="row" justifyContent="flex-end" alignItems="center" spacing={2}>
            {children}
        </Stack>
    );
};

export default Toolbar;
