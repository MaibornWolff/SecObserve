/** @jsxRuntime classic */
import "react-app-polyfill/ie11";
import "react-app-polyfill/stable";
import "proxy-polyfill";
// IE11 needs "jsxRuntime classic" for this initial file which means that "React" needs to be in scope
// https://github.com/facebook/create-react-app/issues/9906

import * as React from "react";
import { createRoot } from "react-dom/client";
import { MsalProvider } from "@azure/msal-react";

import App from "./App";
import { getPublicClientApplication } from "./access_control/aad";

const container = document.getElementById("root");
if (container) {
    const root = createRoot(container);
    const publicClientApplication = getPublicClientApplication();

    root.render(
        <React.StrictMode>
            <MsalProvider instance={publicClientApplication}>
                <App />
            </MsalProvider>
        </React.StrictMode>
    );
}
