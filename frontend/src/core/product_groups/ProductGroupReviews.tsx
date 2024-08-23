import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Accordion, AccordionDetails, AccordionSummary, Chip, Stack, Typography } from "@mui/material";
import { Fragment } from "react";

import { getElevation } from "../../metrics/functions";
import ProductRuleApprovalList from "../../rules/product_rules/ProductRuleApprovalList";

type ProductGroupReviewsProps = {
    product_group: any;
};

const get_chip_color = (value: number) => {
    if (value > 0) {
        return "secondary";
    }
    return "default";
};

const ProductGroupReviews = ({ product_group: product_group }: ProductGroupReviewsProps) => {
    return (
        <Fragment>
            {(product_group.product_rules_need_approval || product_group.product_group_product_rules_need_approval) && (
                <Accordion
                    elevation={getElevation()}
                    sx={{ marginTop: 2 }}
                    defaultExpanded={product_group.product_rule_approvals > 0}
                >
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Stack direction="row" sx={{ display: "flex", alignItems: "center" }}>
                            <Typography variant="h6">Product rules to be approved:</Typography>&nbsp;&nbsp;&nbsp;
                            <Chip
                                label={product_group.product_rule_approvals}
                                color={get_chip_color(product_group.product_rule_approvals)}
                            />
                        </Stack>
                    </AccordionSummary>
                    <AccordionDetails>
                        <ProductRuleApprovalList product={product_group} />
                    </AccordionDetails>
                </Accordion>
            )}
        </Fragment>
    );
};

export default ProductGroupReviews;
