import { Show, SimpleShowLayout, TextField } from "react-admin";

import { useStyles } from "../../commons/layout/themes";

const ParserShow = () => {
    const { classes } = useStyles();
    return (
        <Show>
            <SimpleShowLayout>
                <TextField source="name" className={classes.fontBigBold} />
                <TextField source="type" />
                <TextField source="source" />
            </SimpleShowLayout>
        </Show>
    );
};

export default ParserShow;
