import { MsalProvider } from "@azure/msal-react";
import { createRoot } from "react-dom/client";

import App from "./App";
import { getPublicClientApplication } from "./access_control/aad";

const container = document.getElementById("root");
if (container) {
    const root = createRoot(container);
    const publicClientApplication = getPublicClientApplication();

    root.render(
        <MsalProvider instance={publicClientApplication}>
            <App />
        </MsalProvider>
    );
}
