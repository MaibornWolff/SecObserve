import GroupIcon from "@mui/icons-material/Group";
import { Box, Divider, Paper, Tab, Tabs } from "@mui/material";
import { Fragment, useState } from "react";

import AuthorizationGroupEmbeddedList from "../../access_control/authorization_groups/AuthorizationGroupEmbeddedList";
import users from "../../access_control/users";
import UserEmbeddedList from "../../access_control/users/UserEmbeddedList";
import administration from "../administration";
import ListHeader from "../layout/ListHeader";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function CustomTabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
        </div>
    );
}

function a11yProps(index: number) {
    return {
        id: `simple-tab-${index}`,
        "aria-controls": `simple-tabpanel-${index}`,
    };
}

const Administration = () => {
    const [value, setValue] = useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    return (
        <Fragment>
            <ListHeader icon={administration.icon} title="Administration" />
            <Paper sx={{ marginTop: 2 }}>
                <Tabs value={value} onChange={handleChange} variant="scrollable" scrollButtons="auto">
                    <Tab label="Users" icon={<users.icon />} {...a11yProps(0)} />
                    <Tab label="Administration Groups" icon={<GroupIcon />} {...a11yProps(1)} />
                </Tabs>
                <Divider />
                <CustomTabPanel value={value} index={0}>
                    <UserEmbeddedList />
                </CustomTabPanel>
                <CustomTabPanel value={value} index={1}>
                    <AuthorizationGroupEmbeddedList />
                </CustomTabPanel>
            </Paper>
        </Fragment>
    );
};

export default Administration;
