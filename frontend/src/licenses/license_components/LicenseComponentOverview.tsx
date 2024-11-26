import { Paper } from "@mui/material";
import { useEffect, useState } from "react";
import {
    AutocompleteInput,
    Datagrid,
    FilterForm,
    ListContextProvider,
    NumberField,
    ReferenceInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    useList,
    useNotify,
} from "react-admin";

import { EvaluationResultField } from "../../commons/custom_fields/EvaluationResultField";
import { AutocompleteInputMedium } from "../../commons/layout/themes";
import { httpClient } from "../../commons/ra-data-django-rest-framework";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { PURL_TYPE_CHOICES } from "../../core/types";
import { getElevation } from "../../metrics/functions";
import { EVALUATION_RESULT_CHOICES } from "../types";
import LicenseComponentEmbeddedList from "./LicenseComponentEmbeddedList";

type LicenseComponentOverviewProps = {
    product: any;
};

const LicenseComponentOverview = ({ product }: LicenseComponentOverviewProps) => {
    const [data, setData] = useState();
    const [count, setCount] = useState(0);
    const [loading, setLoading] = useState(false);
    const [filterBranch, setFilterBranch] = useState(undefined);
    const [filterSPDXId, setFilterSPDXId] = useState(undefined);
    const [filterLicenseExpression, setFilterLicenseExpression] = useState(undefined);
    const [filterUnknownLicense, setFilterUnknownLicense] = useState(undefined);
    const [filterEvaluationResult, setFilterEvaluationResult] = useState(undefined);
    const [filterPURLType, setFilterPURLType] = useState(undefined);
    const notify = useNotify();

    function listFilters(product: any) {
        const filters = [];
        if (product && product.has_branches) {
            filters.push(
                <ReferenceInput
                    source="branch"
                    reference="branches"
                    queryOptions={{ meta: { api_resource: "branch_names" } }}
                    sort={{ field: "name", order: "ASC" }}
                    filter={{ product: product.id }}
                    alwaysOn
                >
                    <AutocompleteInputMedium
                        optionText="name"
                        label="Branch / Version"
                        onChange={(e) => setFilterBranch(e)}
                    />
                </ReferenceInput>
            );
        }
        filters.push(
            <TextInput source="spdx_id" label="SPDX Id" onChange={(e) => setFilterSPDXId(e.target.value)} alwaysOn />
        );
        filters.push(
            <TextInput
                source="license_expression"
                onChange={(e) => setFilterLicenseExpression(e.target.value)}
                alwaysOn
            />
        );
        filters.push(
            <TextInput
                source="unknown_license"
                label="Unknown license"
                onChange={(e) => setFilterUnknownLicense(e.target.value)}
                alwaysOn
            />
        );
        filters.push(
            <AutocompleteInputMedium
                source="evaluation_result"
                label="Evaluation result"
                choices={EVALUATION_RESULT_CHOICES}
                onChange={(e) => setFilterEvaluationResult(e)}
                alwaysOn
            />
        );
        filters.push(
            <AutocompleteInput
                source="purl_type"
                label="Component type"
                choices={PURL_TYPE_CHOICES}
                onChange={(e) => setFilterPURLType(e)}
                alwaysOn
            />
        );
        return filters;
    }

    useEffect(() => {
        if (filterBranch === undefined) {
            const storedFilters = localStorage.getItem("RaStore.license_components.overview");
            if (storedFilters) {
                const filters = JSON.parse(storedFilters);
                setFilterBranch(filters.branch);
                setFilterSPDXId(filters.spdx_id);
                setFilterLicenseExpression(filters.license_expression);
                setFilterUnknownLicense(filters.unknown_license);
                setFilterEvaluationResult(filters.evaluation_result);
                setFilterPURLType(filters.purl_type);
            } else {
                setFilterBranch(product.repository_default_branch);
            }
        } else {
            localStorage.removeItem("RaStore.license_components.datagrid.expanded");
            get_data();
        }
    }, [
        // eslint-disable-line react-hooks/exhaustive-deps
        filterBranch,
        filterSPDXId,
        filterLicenseExpression,
        filterUnknownLicense,
        filterEvaluationResult,
        filterPURLType,
    ]);

    function storeFilters() {
        const filterStorage = {
            branch: filterBranch,
            spdx_id: filterSPDXId,
            license_expression: filterLicenseExpression,
            unknown_license: filterUnknownLicense,
            evaluation_result: filterEvaluationResult,
            purl_type: filterPURLType,
        };
        localStorage.setItem("RaStore.license_components.overview", JSON.stringify(filterStorage));
    }

    function get_data() {
        setLoading(true);

        let url =
            window.__RUNTIME_CONFIG__.API_BASE_URL + "/license_components/license_overview/?product=" + product.id;
        if (filterBranch) {
            url += "&branch=" + filterBranch;
        }
        if (filterSPDXId) {
            url += "&spdx_id=" + encodeURIComponent(filterSPDXId);
        }
        if (filterLicenseExpression) {
            url += "&license_expression=" + encodeURIComponent(filterLicenseExpression);
        }
        if (filterUnknownLicense) {
            url += "&unknown_license=" + encodeURIComponent(filterUnknownLicense);
        }
        if (filterEvaluationResult) {
            url += "&evaluation_result=" + encodeURIComponent(filterEvaluationResult);
        }
        if (filterPURLType) {
            url += "&purl_type=" + encodeURIComponent(filterPURLType);
        }

        httpClient(url, {
            method: "GET",
        })
            .then((result: any) => {
                setCount(result.json.count);
                setData(result.json.results);
            })
            .catch((error: any) => {
                if (error !== undefined) {
                    notify(error.message, {
                        type: "warning",
                    });
                } else {
                    notify("Error while loading metrics status", {
                        type: "warning",
                    });
                }
            });

        storeFilters();
        setLoading(false);
    }

    const listContext = useList({
        data,
        isLoading: loading,
        filter: {
            branch: filterBranch,
            spdx_id: filterSPDXId,
            license_expression: filterLicenseExpression,
            unknown_license: filterUnknownLicense,
            evaluation_result: filterEvaluationResult,
            purl_type: filterPURLType,
        },
    });

    return (
        <div style={{ width: "100%" }}>
            <ResourceContextProvider value="license_components">
                <ListContextProvider value={listContext}>
                    <FilterForm filters={listFilters(product)} />
                    <Datagrid
                        data={data}
                        total={count}
                        isLoading={loading}
                        size={getSettingListSize()}
                        bulkActionButtons={false}
                        rowClick={false}
                        expand={
                            <Paper elevation={getElevation(false)}>
                                <LicenseComponentEmbeddedList
                                    product={product}
                                    expand={true}
                                    purl_type={filterPURLType}
                                />
                            </Paper>
                        }
                        expandSingle
                    >
                        {product && product.has_branches && (
                            <TextField source="branch_name" label="Branch / Version" sortable={false} />
                        )}
                        <TextField source="spdx_id" label="SPDX Id" sortable={false} />
                        <TextField source="license_name" label="License name" sortable={false} />
                        <TextField source="license_expression" label="Expression" sortable={false} />
                        <TextField source="unknown_license" label="Unknown license" sortable={false} />
                        <EvaluationResultField source="evaluation_result" label="Evaluation result" sortable={false} />
                        <NumberField source="num_components" label="# Components" sortable={false} />
                    </Datagrid>
                </ListContextProvider>
            </ResourceContextProvider>
        </div>
    );
};

export default LicenseComponentOverview;
