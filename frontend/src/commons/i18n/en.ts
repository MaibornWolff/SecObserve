import { TranslationMessages } from "react-admin";
import englishMessages from "ra-language-english";

const customEnglishMessages: TranslationMessages = {
    ...englishMessages,
    pos: {
        search: "Search",
        configuration: "Configuration",
        language: "Language",
        theme: {
            name: "Theme",
            light: "Light",
            dark: "Dark",
        },
        dashboard: {},
        menu: {
            sales: "Sales",
            catalog: "Catalog",
            customers: "Customers",
        },
    },
    resources: {
        products: {
            name: "Product |||| Products",
            fields: {
                name: "Name",
                description: "Description",
            },
            page: {
                delete: "Delete Product",
            },
        },
        observations: {
            name: "Observation |||| Observations",
            fields: {
                name: "Title",
            },
            page: {
                delete: "Delete Observation",
            },
        },
        parsers: {
            name: "Parser |||| Parsers",
            fields: {
                name: "Name",
                type: "Type",
            },
            page: {
                delete: "Delete Parser",
            },
        },
    },
};

export default customEnglishMessages;
