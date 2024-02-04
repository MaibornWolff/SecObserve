import Box from "@mui/material/Box";
import { Fragment } from "react";
import { DashboardMenuItem, MenuItemLink, MenuProps, useSidebarState, useTranslate } from "react-admin";

import observations from "../../core/observations";
import parsers from "../../core/parsers";
import product_groups from "../../core/product_groups";
import products from "../../core/products";
import general_rules from "../../rules/general_rules";
import notifications from "../notifications";

const Menu = ({ dense = false }: MenuProps) => {
    const translate = useTranslate();
    const [open] = useSidebarState();

    return (
        <Fragment>
            <Box
                sx={{
                    width: open ? 200 : 50,
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
                    primaryText={translate(`resources.products.name`, {
                        smart_count: 2,
                    })}
                    leftIcon={<products.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/observations"
                    state={{ _scrollToTop: true }}
                    primaryText={translate(`resources.observations.name`, {
                        smart_count: 2,
                    })}
                    leftIcon={<observations.icon />}
                    dense={dense}
                />
                <MenuItemLink
                    to="/parsers"
                    state={{ _scrollToTop: true }}
                    primaryText={translate(`resources.parsers.name`, {
                        smart_count: 2,
                    })}
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
                <MenuItemLink
                    to="/notifications"
                    state={{ _scrollToTop: true }}
                    primaryText="Notifications"
                    leftIcon={<notifications.icon />}
                    dense={dense}
                />
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
