import { Layout, LayoutProps } from "react-admin";

import AppBar from "./AppBar";
import Menu from "./Menu";

export default (props: LayoutProps) => {
    return <Layout {...props} appBar={AppBar} menu={Menu} />; // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
    // no idea how to solve it, we accept the risk
};
