import { Box, Divider, Paper, Tab, Tabs } from "@mui/material";
import { ReactNode } from "react";
import { Fragment } from "react";
import { Link, matchPath, useLocation } from "react-router-dom";

import administration from ".";
import ListHeader from "../../commons/layout/ListHeader";
import concluded_licenses from "../concluded_licenses";
import ConcludedLicenseEmbeddedList from "../concluded_licenses/ConcludedLicenseEmbeddedList";
import license_groups from "../license_groups";
import LicenseGroupEmbeddedList from "../license_groups/LicenseGroupEmbeddedList";
import license_policies from "../license_policies";
import LicensePolicyEmbeddedList from "../license_policies/LicensePolicyEmbeddedList";
import licenses from "../licenses";
import LicenseEmbeddedList from "../licenses/LicenseEmbeddedList";

function useRouteMatch(patterns: readonly string[]) {
    const { pathname } = useLocation();

    for (const pattern of patterns) {
        const possibleMatch = matchPath(pattern, pathname);
        if (possibleMatch !== null) {
            return possibleMatch;
        }
    }
    return null;
}

interface TabPanelProps {
    children?: ReactNode;
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
            {...other} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
            // nosemgrep because the props are well defined in the import
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

export default function LicenseAdministration() {
    const routeMatch = useRouteMatch([
        "/license/licenses",
        "/license/license_groups",
        "/license/license_policies",
        "/license/concluded_licenses",
    ]);
    function currentTab(): number {
        switch (routeMatch?.pattern?.path) {
            case "/license/licenses": {
                return 0;
            }
            case "/license/license_groups": {
                return 1;
            }
            case "/license/license_policies": {
                return 2;
            }
            case "/license/concluded_licenses": {
                return 3;
            }
            default: {
                return 0;
            }
        }
    }

    return (
        <Fragment>
            <ListHeader icon={administration.icon} title="License management" />
            <Paper sx={{ marginTop: 2 }}>
                <Tabs value={currentTab()} variant="scrollable" scrollButtons="auto">
                    <Tab
                        label="SPDX Licenses"
                        icon={<licenses.icon />}
                        to="/license/licenses"
                        component={Link}
                        {...a11yProps(0)} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                        // nosemgrep because the props are well defined in the import
                    />
                    <Tab
                        label="License Groups"
                        icon={<license_groups.icon />}
                        to="/license/license_groups"
                        component={Link}
                        {...a11yProps(1)} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                        // nosemgrep because the props are well defined in the import
                    />
                    <Tab
                        label="License Policies"
                        icon={<license_policies.icon />}
                        to="/license/license_policies"
                        component={Link}
                        {...a11yProps(2)} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                        // nosemgrep because the props are well defined in the import
                    />
                    <Tab
                        label="Concluded Licenses"
                        icon={<concluded_licenses.icon />}
                        to="/license/concluded_licenses"
                        component={Link}
                        {...a11yProps(3)} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                        // nosemgrep because the props are well defined in the import
                    />
                </Tabs>
                <Divider />
                <CustomTabPanel value={currentTab()} index={0}>
                    <LicenseEmbeddedList license_group={null} />
                </CustomTabPanel>
                <CustomTabPanel value={currentTab()} index={1}>
                    <LicenseGroupEmbeddedList license={null} />
                </CustomTabPanel>
                <CustomTabPanel value={currentTab()} index={2}>
                    <LicensePolicyEmbeddedList license={null} license_group={null} />
                </CustomTabPanel>
                <CustomTabPanel value={currentTab()} index={3}>
                    <ConcludedLicenseEmbeddedList />
                </CustomTabPanel>
            </Paper>
        </Fragment>
    );
}
