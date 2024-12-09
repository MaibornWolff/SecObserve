import ChecklistIcon from "@mui/icons-material/Checklist";
import SecurityIcon from "@mui/icons-material/Security";
import SettingsIcon from "@mui/icons-material/Settings";
import Box from "@mui/material/Box";
import { Fragment, useState } from "react";
import { DashboardMenuItem, MenuItemLink, MenuProps, useSidebarState } from "react-admin";

import administration from "../../access_control/access_control_administration";
import observations from "../../core/observations";
import product_groups from "../../core/product_groups";
import products from "../../core/products";
import parsers from "../../import_observations/parsers";
import licenses from "../../licenses/licenses";
import general_rules from "../../rules/general_rules";
import csaf from "../../vex/csaf";
import openvex from "../../vex/openvex";
import vex_counters from "../../vex/vex_counters";
import vex_documents from "../../vex/vex_documents";
import { feature_license_management, feature_vex_enabled } from "../functions";
import { is_superuser } from "../functions";
import notifications from "../notifications";
import settings from "../settings";
import SubMenu from "./SubMenu";

type MenuName = "menuSettings" | "menuVEX";

const Menu = ({ dense = false }: MenuProps) => {
    const [open] = useSidebarState();
    const [state, setState] = useState({ menuSettings: false, menuVEX: false });
    const handleToggle = (menu: MenuName) => {
        setState((state) => ({ ...state, [menu]: !state[menu] })); // eslint-disable-line security/detect-object-injection
    };

    return (
        <Fragment>
            <Box
                sx={{
                    width: open ? 220 : 50,
                    marginTop: 1,
                    marginBottom: 1,
                    transition: (theme) =>
                        theme.transitions.create("width", {
                            easing: theme.transitions.easing.sharp,
                            duration: theme.transitions.duration.leavingScreen,
                        }),
                }}
            >
                <DashboardMenuItem />
                <MenuItemLink
                    to="/product_groups"
                    state={{ _scrollToTop: true }}
                    primaryText="Product Groups"
                    leftIcon={<product_groups.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/products"
                    state={{ _scrollToTop: true }}
                    primaryText="Products"
                    leftIcon={<products.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/observations"
                    state={{ _scrollToTop: true }}
                    primaryText="Observations"
                    leftIcon={<observations.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/observation_logs/needs_approval"
                    state={{ _scrollToTop: true }}
                    primaryText="Reviews"
                    leftIcon={<ChecklistIcon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/notifications"
                    state={{ _scrollToTop: true }}
                    primaryText="Notifications"
                    leftIcon={<notifications.icon />}
                    dense={dense}
                />
                {feature_vex_enabled() && (
                    <SubMenu
                        handleToggle={() => handleToggle("menuVEX")}
                        isOpen={state.menuVEX}
                        name="VEX"
                        icon={<SecurityIcon />}
                        dense={dense}
                    >
                        <MenuItemLink
                            to="/vex/csaf"
                            state={{ _scrollToTop: true }}
                            primaryText="CSAF"
                            leftIcon={<csaf.icon />}
                            dense={dense}
                        />
                        <MenuItemLink
                            to="/vex/openvex"
                            state={{ _scrollToTop: true }}
                            primaryText="OpenVEX"
                            leftIcon={<openvex.icon />}
                            dense={dense}
                        />
                        {is_superuser() && (
                            <MenuItemLink
                                to="/vex/vex_documents"
                                state={{ _scrollToTop: true }}
                                primaryText="VEX documents"
                                leftIcon={<vex_documents.icon />}
                                dense={dense}
                            />
                        )}
                    </SubMenu>
                )}
                <SubMenu
                    handleToggle={() => handleToggle("menuSettings")}
                    isOpen={state.menuSettings}
                    name="Administration"
                    icon={<SettingsIcon />}
                    dense={dense}
                >
                    {feature_license_management() && (
                        <MenuItemLink
                            to="/license/licenses"
                            state={{ _scrollToTop: true }}
                            primaryText="Licenses"
                            leftIcon={<licenses.icon />}
                            dense={dense}
                        />
                    )}
                    <MenuItemLink
                        to="/access_control/users"
                        state={{ _scrollToTop: true }}
                        primaryText="Access Control"
                        leftIcon={<administration.icon />}
                        dense={dense}
                    />
                    {is_superuser() && (
                        <MenuItemLink
                            to="/settings/1/show"
                            state={{ _scrollToTop: true }}
                            primaryText="Settings"
                            leftIcon={<settings.icon />}
                            dense={dense}
                        />
                    )}
                    <MenuItemLink
                        to="/parsers"
                        state={{ _scrollToTop: true }}
                        primaryText="Parsers"
                        leftIcon={<parsers.icon />}
                        dense={dense}
                    />
                    <MenuItemLink
                        to="/general_rules"
                        state={{ _scrollToTop: true }}
                        primaryText="General Rules"
                        leftIcon={<general_rules.icon />}
                        dense={dense}
                    />
                    {feature_vex_enabled() && (
                        <MenuItemLink
                            to="/vex/vex_counters"
                            state={{ _scrollToTop: true }}
                            primaryText="VEX Counters"
                            leftIcon={<vex_counters.icon />}
                            dense={dense}
                        />
                    )}
                </SubMenu>
            </Box>
            <Box
                style={{
                    position: "fixed",
                    right: 0,
                    bottom: 0,
                    left: 0,
                    zIndex: 100,
                    paddingLeft: 16,
                    paddingBottom: 14,
                }}
            >
                <a href="https://www.maibornwolff.de" target="_blank" rel="noreferrer">
                    <img src="maibornwolff.svg" height={"24px"} />
                </a>
            </Box>
        </Fragment>
    );
};

export default Menu;
