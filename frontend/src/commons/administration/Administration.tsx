import { Box, Divider, Paper, Tab, Tabs } from "@mui/material";
import { Fragment } from "react";
import { Link, matchPath, useLocation } from "react-router-dom";

import api_tokens from "../../access_control/api_tokens";
import ApiTokenEmbeddedList from "../../access_control/api_tokens/ApiTokenEmbeddedList";
import authorization_groups from "../../access_control/authorization_groups";
import AuthorizationGroupEmbeddedList from "../../access_control/authorization_groups/AuthorizationGroupEmbeddedList";
import users from "../../access_control/users";
import UserEmbeddedList from "../../access_control/users/UserEmbeddedList";
import administration from "../administration";
import ListHeader from "../layout/ListHeader";

function useRouteMatch(patterns: readonly string[]) {
    const { pathname } = useLocation();
    for (let i = 0; i < patterns.length; i += 1) {
        const pattern = patterns[i];
        const possibleMatch = matchPath(pattern, pathname);
        if (possibleMatch !== null) {
            return possibleMatch;
        }
    }
    return null;
}

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
            {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
        </div>
    );
}

function a11yProps(index: number) {
    return {
        id: `simple-tab-${index}`,
        "aria-controls": `simple-tabpanel-${index}`,
    };
}

export default function Administration() {
    const user = localStorage.getItem("user");

    const routeMatch = useRouteMatch([
        "/administration/users",
        "/administration/authorization_groups",
        "/administration/api_tokens",
    ]);
    function currentTab(): number {
        switch (routeMatch?.pattern?.path) {
            case "/administration/users": {
                return 0;
            }
            case "/administration/authorization_groups": {
                return 1;
            }
            case "/administration/api_tokens": {
                return 2;
            }
            default: {
                return 0;
            }
        }
    }

    return (
        <Fragment>
            <ListHeader icon={administration.icon} title="Administration" />
            <Paper sx={{ marginTop: 2 }}>
                <Tabs value={currentTab()} variant="scrollable" scrollButtons="auto">
                    <Tab
                        label="Users"
                        icon={<users.icon />}
                        to="/administration/users"
                        component={Link}
                        {...a11yProps(0)}
                    />
                    <Tab
                        label="Authorization Groups"
                        icon={<authorization_groups.icon />}
                        to="/administration/authorization_groups"
                        component={Link}
                        {...a11yProps(1)}
                    />
                    {user && JSON.parse(user).is_superuser && <Tab
                        label="API Tokens"
                        icon={<api_tokens.icon />}
                        to="/administration/api_tokens"
                        component={Link}
                        {...a11yProps(2)}
                    />}
                </Tabs>
                <Divider />
                <CustomTabPanel value={currentTab()} index={0}>
                    <UserEmbeddedList />
                </CustomTabPanel>
                <CustomTabPanel value={currentTab()} index={1}>
                    <AuthorizationGroupEmbeddedList />
                </CustomTabPanel>
                <CustomTabPanel value={currentTab()} index={2}>
                    <ApiTokenEmbeddedList />
                </CustomTabPanel>
            </Paper>
        </Fragment>
    );
}
