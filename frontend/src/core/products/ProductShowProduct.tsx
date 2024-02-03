import { Divider, Stack, Typography } from "@mui/material";
import { Fragment } from "react";
import { BooleanField, Labeled, NumberField, ReferenceField, RichTextField, TextField } from "react-admin";

import { SeverityField } from "../../commons/custom_fields/SeverityField";
import { Product } from "../types";

type ProductShowProductProps = {
    product: Product;
};

const ProductShowProduct = ({ product }: ProductShowProductProps) => {
    return (
        <Fragment>
            <Typography variant="h6">Product</Typography>
            <Stack spacing={1}>
                <Labeled>
                    <TextField source="name" />
                </Labeled>
                {product.description && (
                    <Labeled>
                        <RichTextField source="description" />
                    </Labeled>
                )}
                {product.product_group && (
                    <Labeled label="Product group">
                        <ReferenceField source="product_group" reference="product_groups" link="show">
                            <TextField source="name" />
                        </ReferenceField>
                    </Labeled>
                )}
            </Stack>

            <Divider sx={{ marginTop: 2, marginBottom: 2 }} />

            <Typography variant="h6">Rules</Typography>
            <Labeled label="Apply general rules">
                <BooleanField source="apply_general_rules" />
            </Labeled>

            {(product.repository_prefix ||
                product.repository_default_branch ||
                product.repository_branch_housekeeping_active != null) && (
                <Fragment>
                    <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6">Source code repository</Typography>
                    <Stack spacing={1}>
                        {product.repository_prefix && (
                            <Labeled>
                                <TextField source="repository_prefix" />
                            </Labeled>
                        )}
                        {product.repository_default_branch && (
                            <ReferenceField source="repository_default_branch" reference="branches" link={false}>
                                <Labeled label="Default branch">
                                    <TextField source="name" />
                                </Labeled>
                            </ReferenceField>
                        )}
                    </Stack>
                    {((!product.product_group && product.repository_branch_housekeeping_active != null) ||
                        (product.product_group &&
                            product.product_group_repository_branch_housekeeping_active == null &&
                            product.repository_branch_housekeeping_active != null)) && (
                        <Fragment>
                            <Labeled label="Housekeeping">
                                <BooleanField
                                    source="repository_branch_housekeeping_active"
                                    valueLabelFalse="Disabled"
                                    valueLabelTrue="Product specific"
                                />
                            </Labeled>
                            {product.repository_branch_housekeeping_active == true && (
                                <Stack spacing={1}>
                                    <Labeled label="Keep inactive">
                                        <NumberField source="repository_branch_housekeeping_keep_inactive_days" />
                                    </Labeled>
                                    <Labeled label="Exempt branches">
                                        <TextField source="repository_branch_housekeeping_exempt_branches" />
                                    </Labeled>
                                </Stack>
                            )}
                        </Fragment>
                    )}
                    {product.product_group && product.product_group_repository_branch_housekeeping_active != null && (
                        <Labeled label="Housekeeping (from product group)">
                            <BooleanField
                                source="product_group_repository_branch_housekeeping_active"
                                valueLabelFalse="Disabled"
                                valueLabelTrue="Product group specific"
                            />
                        </Labeled>
                    )}
                </Fragment>
            )}

            {(product.notification_email_to ||
                product.notification_ms_teams_webhook ||
                product.notification_slack_webhook) && (
                <Fragment>
                    <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6">Notifications</Typography>
                    <Stack spacing={1}>
                        {product.notification_email_to && (
                            <Labeled label="Email">
                                <TextField source="notification_email_to" />
                            </Labeled>
                        )}
                        {product.notification_ms_teams_webhook && (
                            <Labeled label="MS Teams">
                                <TextField source="notification_ms_teams_webhook" />
                            </Labeled>
                        )}
                        {product.notification_slack_webhook && (
                            <Labeled label="Slack">
                                <TextField source="notification_slack_webhook" />
                            </Labeled>
                        )}
                    </Stack>
                </Fragment>
            )}

            {((!product.product_group && product.security_gate_active != null) ||
                (product.product_group &&
                    product.product_group_security_gate_active == null &&
                    product.security_gate_active != null)) && (
                <Fragment>
                    <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6">Security Gate</Typography>
                    <Labeled label="Security gate">
                        <BooleanField
                            source="security_gate_active"
                            valueLabelFalse="Disabled"
                            valueLabelTrue="Product specific"
                        />
                    </Labeled>
                    {product.security_gate_active == true && (
                        <Stack spacing={1}>
                            <Labeled>
                                <NumberField source="security_gate_threshold_critical" />
                            </Labeled>
                            <Labeled>
                                <NumberField source="security_gate_threshold_high" />
                            </Labeled>
                            <Labeled>
                                <NumberField source="security_gate_threshold_medium" />
                            </Labeled>
                            <Labeled>
                                <NumberField source="security_gate_threshold_low" />
                            </Labeled>
                            <Labeled>
                                <NumberField source="security_gate_threshold_none" />
                            </Labeled>
                            <Labeled>
                                <NumberField source="security_gate_threshold_unkown" />
                            </Labeled>
                        </Stack>
                    )}
                </Fragment>
            )}

            {product.product_group && product.product_group_security_gate_active != null && (
                <Fragment>
                    <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
                    <Typography variant="h6">Security Gate</Typography>
                    <Labeled label="Security gate (from product group)">
                        <BooleanField
                            source="product_group_security_gate_active"
                            valueLabelFalse="Disabled"
                            valueLabelTrue="Product group specific"
                        />
                    </Labeled>
                </Fragment>
            )}

            <Divider sx={{ marginTop: 2, marginBottom: 2 }} />
            <Typography variant="h6">Issue Tracker</Typography>
            <Labeled label="Active">
                <BooleanField source="issue_tracker_active" />
            </Labeled>
            {product.issue_tracker_active && (
                <Stack spacing={1}>
                    <Labeled>
                        <TextField source="issue_tracker_type" label="Type" />
                    </Labeled>
                    <Labeled>
                        <TextField source="issue_tracker_base_url" label="Base URL" />
                    </Labeled>
                    <Labeled>
                        <TextField source="issue_tracker_project_id" label="Project id" />
                    </Labeled>
                    <Labeled>
                        <TextField source="issue_tracker_labels" label="Labels" />
                    </Labeled>
                    {product && product.issue_tracker_minimum_severity && (
                        <Labeled>
                            <SeverityField source="issue_tracker_minimum_severity" label="Minimum severity" />
                        </Labeled>
                    )}
                    {product.issue_tracker_username && (
                        <Labeled>
                            <TextField source="issue_tracker_username" label="Username (only for Jira)" />
                        </Labeled>
                    )}
                    {product.issue_tracker_issue_type && (
                        <Labeled>
                            <TextField source="issue_tracker_issue_type" label="Issue type (only for Jira)" />
                        </Labeled>
                    )}
                    {product.issue_tracker_status_closed && (
                        <Labeled>
                            <TextField source="issue_tracker_status_closed" label="Closed status (only for Jira)" />
                        </Labeled>
                    )}
                </Stack>
            )}
        </Fragment>
    );
};

export default ProductShowProduct;
