import { Box, Paper, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import {
    BooleanField,
    EditButton,
    Labeled,
    PrevNextButtons,
    Show,
    TextField,
    TopToolbar,
    WithRecord,
    useRecordContext,
} from "react-admin";

import MarkdownField from "../../commons/custom_fields/MarkdownField";
import { is_external, is_superuser } from "../../commons/functions";
import { useStyles } from "../../commons/layout/themes";
import ProductGroupEmbeddedList from "../../core/product_groups/ProductGroupEmbeddedList";
import ProductEmbeddedList from "../../core/products/ProductEmbeddedList";
import LicensePolicyAuthorizationGroupMemberEmbeddedList from "../license_policy_authorization_group_members/LicensePolicyAuthorizationGroupMemberEmbeddedList";
import LicensePolicyItemEmbeddedList from "../license_policy_items/LicensePolicyItemEmbeddedList";
import LicensePolicyMemberEmbeddedList from "../license_policy_members/LicensePolicyMemberEmbeddedList";
import LicensePolicyApply from "./LicensePolicyApply";
import LicensePolicyCopy from "./LicensePolicyCopy";

const ShowActions = () => {
    const license_policy = useRecordContext();
    return (
        <TopToolbar>
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <PrevNextButtons
                    linkType="show"
                    sort={{ field: "name", order: "ASC" }}
                    filterDefaultValues={{ is_active: true }}
                    storeKey="license_policies.embedded"
                />
                {license_policy && (license_policy.is_manager || is_superuser()) && license_policy.has_products && (
                    <LicensePolicyApply license_policy={license_policy} />
                )}
                {license_policy && (!is_external() || is_superuser()) && (
                    <LicensePolicyCopy license_policy={license_policy} />
                )}
                {((license_policy && license_policy.is_manager) || is_superuser()) && <EditButton />}
            </Stack>
        </TopToolbar>
    );
};

const LicensePolicyComponent = () => {
    const { classes } = useStyles();

    return (
        <WithRecord
            render={(license_policy) => (
                <Box width={"100%"}>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            License Policy
                        </Typography>
                        <Stack spacing={1}>
                            <Labeled label="Name">
                                <TextField source="name" className={classes.fontBigBold} />
                            </Labeled>
                            {license_policy.description && (
                                <Labeled>
                                    <MarkdownField content={license_policy.description} label="Description" />
                                </Labeled>
                            )}
                            {license_policy.ignore_component_types && (
                                <Labeled>
                                    <TextField source="ignore_component_types" />
                                </Labeled>
                            )}
                            <Labeled label="Public">
                                <BooleanField source="is_public" />
                            </Labeled>
                        </Stack>
                    </Paper>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Items
                        </Typography>
                        <LicensePolicyItemEmbeddedList license_policy={license_policy} />
                    </Paper>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Users
                        </Typography>
                        <LicensePolicyMemberEmbeddedList license_policy={license_policy} />
                    </Paper>
                    <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                        <Typography variant="h6" sx={{ marginBottom: 1 }}>
                            Authorization Groups
                        </Typography>
                        <LicensePolicyAuthorizationGroupMemberEmbeddedList license_policy={license_policy} />
                    </Paper>
                    {license_policy.has_product_groups && (
                        <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Product Groups using this license policy
                            </Typography>
                            <ProductGroupEmbeddedList license_policy={license_policy} />
                        </Paper>
                    )}
                    {license_policy.has_products && (
                        <Paper sx={{ marginBottom: 2, padding: 2, width: "100%" }}>
                            <Typography variant="h6" sx={{ marginBottom: 1 }}>
                                Products using this license policy
                            </Typography>
                            <ProductEmbeddedList license_policy={license_policy} />
                        </Paper>
                    )}
                </Box>
            )}
        />
    );
};

const LicensePolicyShow = () => {
    return (
        <Show actions={<ShowActions />} component={LicensePolicyComponent}>
            <Fragment />
        </Show>
    );
};

export default LicensePolicyShow;
