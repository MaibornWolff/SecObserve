import { CheckForApplicationUpdate, Layout, LayoutProps } from "react-admin";

import AppBar from "./AppBar";
import Menu from "./Menu";

export default ({ children }: LayoutProps) => {
    return (
        <Layout appBar={AppBar} menu={Menu}>
            {children}
            <CheckForApplicationUpdate interval={5*60*1000} />
        </Layout>
    );
};
