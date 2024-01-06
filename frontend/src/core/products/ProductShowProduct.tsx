import { Typography } from "@mui/material";
import {
    BooleanField,
    Labeled,
    NumberField,
    ReferenceField,
    RichTextField,
    SimpleShowLayout,
    TextField,
} from "react-admin";

import { Product } from "../types";

type ProductShowProductProps = {
    product: Product;
};

const ProductShowProduct = ({ product }: ProductShowProductProps) => {
    return (
        <SimpleShowLayout>
            <Typography variant="h6">Product</Typography>
            <TextField source="name" />
            {product.description && <RichTextField source="description" />}
            {product.product_group && (
                <ReferenceField source="product_group" reference="product_groups" link="show">
                    <TextField source="name" />
                </ReferenceField>
            )}

            <Typography variant="h6" sx={{ marginTop: "1em" }}>
                Rules
            </Typography>
            <BooleanField source="apply_general_rules" />

            {(product.repository_prefix ||
                product.repository_default_branch ||
                product.repository_branch_housekeeping_active != null) && (
                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Source code repository
                </Typography>
            )}
            {product.repository_prefix && <TextField source="repository_prefix" />}
            {product.repository_default_branch && (
                <ReferenceField source="repository_default_branch" reference="branches" link={false}>
                    <TextField source="name" />
                </ReferenceField>
            )}
            {((!product.product_group && product.repository_branch_housekeeping_active != null) ||
                (product.product_group &&
                    product.product_group_repository_branch_housekeeping_active == null &&
                    product.repository_branch_housekeeping_active != null)) && (
                <div>
                    <Labeled label="Housekeeping">
                        <BooleanField
                            source="repository_branch_housekeeping_active"
                            valueLabelFalse="Disabled"
                            valueLabelTrue="Product specific"
                        />
                    </Labeled>
                    {product.repository_branch_housekeeping_active == true && (
                        <div>
                            <Labeled label="Keep inactive">
                                <NumberField source="repository_branch_housekeeping_keep_inactive_days" />
                            </Labeled>
                            <br />
                            <Labeled label="Exempt branches">
                                <TextField source="repository_branch_housekeeping_exempt_branches" />
                            </Labeled>
                            <br />
                        </div>
                    )}
                </div>
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

            {(product.notification_email_to ||
                product.notification_ms_teams_webhook ||
                product.notification_slack_webhook) && (
                <Typography variant="h6" sx={{ marginTop: "1em" }}>
                    Notifications
                </Typography>
            )}
            {product.notification_email_to && <TextField source="notification_email_to" label="Email" />}
            {product.notification_ms_teams_webhook && (
                <TextField source="notification_ms_teams_webhook" label="MS Teams" />
            )}
            {product.notification_slack_webhook && <TextField source="notification_slack_webhook" label="Slack" />}

            {((!product.product_group && product.security_gate_active != null) ||
                (product.product_group &&
                    product.product_group_security_gate_active == null &&
                    product.security_gate_active != null)) && (
                <div>
                    <Typography variant="h6" sx={{ marginTop: "1em" }}>
                        Security Gate
                    </Typography>
                    <Labeled label="Security gate">
                        <BooleanField
                            source="security_gate_active"
                            valueLabelFalse="Disabled"
                            valueLabelTrue="Product specific"
                        />
                    </Labeled>
                    {product.security_gate_active == true && (
                        <div>
                            <Labeled>
                                <NumberField source="security_gate_threshold_critical" />
                            </Labeled>
                            <br />
                            <Labeled>
                                <NumberField source="security_gate_threshold_high" />
                            </Labeled>
                            <br />
                            <Labeled>
                                <NumberField source="security_gate_threshold_medium" />
                            </Labeled>
                            <br />
                            <Labeled>
                                <NumberField source="security_gate_threshold_low" />
                            </Labeled>
                            <br />
                            <Labeled>
                                <NumberField source="security_gate_threshold_none" />
                            </Labeled>
                            <br />
                            <Labeled>
                                <NumberField source="security_gate_threshold_unkown" />
                            </Labeled>
                            <br />
                        </div>
                    )}
                </div>
            )}
            {product.product_group && product.product_group_security_gate_active != null && (
                <div>
                    <Typography variant="h6" sx={{ marginTop: "1em" }}>
                        Security Gate
                    </Typography>
                    <Labeled label="Security gate (from product group)">
                        <BooleanField
                            source="product_group_security_gate_active"
                            valueLabelFalse="Disabled"
                            valueLabelTrue="Product group specific"
                        />
                    </Labeled>
                </div>
            )}

            <Typography variant="h6" sx={{ marginTop: "1em" }}>
                Issue Tracker
            </Typography>
            <BooleanField source="issue_tracker_active" label="Active" />
            {product.issue_tracker_type && (
                <div>
                    <Labeled>
                        <TextField source="issue_tracker_type" label="Type" />
                    </Labeled>
                    <br />
                    <Labeled>
                        <TextField source="issue_tracker_base_url" label="Base URL" />
                    </Labeled>
                    <br />
                    <Labeled>
                        <TextField source="issue_tracker_project_id" label="Project id" />
                    </Labeled>
                    <br />
                    <Labeled>
                        <TextField source="issue_tracker_labels" label="Labels" />
                    </Labeled>
                    <br />
                    {product.issue_tracker_username && (
                        <div>
                            <Labeled>
                                <TextField source="issue_tracker_username" label="Username (only for Jira)" />
                            </Labeled>
                            <br />
                        </div>
                    )}
                    {product.issue_tracker_issue_type && (
                        <div>
                            <Labeled>
                                <TextField source="issue_tracker_issue_type" label="Issue type (only for Jira)" />
                            </Labeled>
                            <br />
                        </div>
                    )}
                    {product.issue_tracker_status_closed && (
                        <div>
                            <Labeled>
                                <TextField source="issue_tracker_status_closed" label="Closed status (only for Jira)" />
                            </Labeled>
                            <br />
                        </div>
                    )}
                </div>
            )}
        </SimpleShowLayout>
    );
};

export default ProductShowProduct;
