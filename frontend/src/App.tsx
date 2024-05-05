import polyglotI18nProvider from "ra-i18n-polyglot";
import { Admin, CustomRoutes, Resource } from "react-admin";
import { AuthProvider } from "react-oidc-context";
import { Route } from "react-router";

import { Login } from "./access_control";
import AccessControlAdministration from "./access_control/access_control_administration/AccessControlAdministration";
import authProvider from "./access_control/authProvider";
import { oidcConfig } from "./access_control/authProvider";
import authorization_groups from "./access_control/authorization_groups";
import users from "./access_control/users";
import englishMessages from "./commons/i18n/en";
import { Layout } from "./commons/layout";
import { darkTheme, lightTheme } from "./commons/layout/themes";
import notifications from "./commons/notifications";
import drfProvider from "./commons/ra-data-django-rest-framework";
import settings from "./commons/settings";
import UserSettings from "./commons/user_settings/UserSettings";
import evidences from "./core/evidences";
import observation_logs from "./core/observation_logs";
import observations from "./core/observations";
import parsers from "./core/parsers";
import product_groups from "./core/product_groups";
import products from "./core/products";
import { Dashboard } from "./dashboard";
import general_rules from "./rules/general_rules";
import product_rules from "./rules/product_rules";
import csaf from "./vex/csaf";
import openvex from "./vex/openvex";
import vex_counters from "./vex/vex_counters";

const i18nProvider = polyglotI18nProvider(() => {
    return englishMessages;
}, "en");

const App = () => {
    return (
        <AuthProvider
            {...oidcConfig} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
            // nosemgrep because the props are well defined in the import
        >
            <Admin
                title=""
                dataProvider={drfProvider()}
                authProvider={authProvider}
                dashboard={Dashboard}
                loginPage={Login}
                layout={Layout}
                i18nProvider={i18nProvider}
                disableTelemetry
                theme={lightTheme}
                darkTheme={darkTheme}
            >
                <CustomRoutes>
                    <Route path="/access_control/users" element={<AccessControlAdministration />} />
                    <Route path="/access_control/authorization_groups" element={<AccessControlAdministration />} />
                    <Route path="/access_control/api_tokens" element={<AccessControlAdministration />} />
                    <Route path="/user_settings" element={<UserSettings />} />
                </CustomRoutes>
                <Resource
                    name="product_groups"
                    {...product_groups} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="products"
                    {...products} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="observations"
                    {...observations} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.title)}`}
                />
                <Resource
                    name="observation_logs"
                    {...observation_logs} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                />
                <Resource
                    name="parsers"
                    {...parsers} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="general_rules"
                    {...general_rules} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="product_rules"
                    {...product_rules} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="evidences"
                    {...evidences} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource name="branches" recordRepresentation={(record) => `${trim_string(record.name)}`} />
                <Resource
                    name="users"
                    {...users} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.full_name)}`}
                />
                <Resource
                    name="authorization_groups"
                    {...authorization_groups} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="settings"
                    {...settings} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                />
                <Resource
                    name="notifications"
                    {...notifications} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.name)}`}
                />
                <Resource
                    name="vex/csaf"
                    {...csaf} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                />
                <Resource
                    name="vex/openvex"
                    {...openvex} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                />
                <Resource
                    name="vex/vex_counters"
                    {...vex_counters} // nosemgrep: typescript.react.best-practice.react-props-spreading.react-props-spreading
                    // nosemgrep because the props are well defined in the import
                    recordRepresentation={(record) => `${trim_string(record.document_id_prefix + "_" + record.year)}`}
                />
            </Admin>
        </AuthProvider>
    );
};

function trim_string(in_string: string) {
    if (in_string === undefined) {
        return "";
    }

    const out_string = in_string.length > 50 ? in_string.substring(0, 50) + "..." : in_string;

    return out_string;
}

export default App;
