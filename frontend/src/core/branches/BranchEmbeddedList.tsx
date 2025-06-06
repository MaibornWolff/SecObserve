import { Stack } from "@mui/material";
import {
    BooleanField,
    Datagrid,
    DateField,
    ListContextProvider,
    ResourceContextProvider,
    TextField,
    WithRecord,
    useListController,
} from "react-admin";

import { PERMISSION_BRANCH_DELETE, PERMISSION_BRANCH_EDIT, PERMISSION_PRODUCT_EDIT } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import LicensesCountField from "../../commons/custom_fields/LicensesCountField";
import OSVLinuxDistributionField from "../../commons/custom_fields/OSVLinuxDistributionField";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { feature_license_management } from "../../commons/functions";
import { getSettingListSize } from "../../commons/user_settings/functions";
import BranchDelete from "./BranchDelete";
import BranchEdit from "./BranchEdit";
import DefaultBranch from "./DefaultBranch";

type BranchEmbeddedListProps = {
    product: any;
};

const BranchEmbeddedList = ({ product }: BranchEmbeddedListProps) => {
    const listContext = useListController({
        filter: { product: Number(product.id) },
        perPage: 25,
        resource: "branches",
        sort: { field: "last_import", order: "DESC" },
        disableSyncWithLocation: true,
        storeKey: "branch.embedded",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    function get_observations_url(product_id: number, branch_id: number): string {
        return `#/products/${product_id}/show?displayedFilters=%7B%7D&filter=%7B%22current_status%22%3A%22Open%22%2C%22branch%22%3A${branch_id}%7D&order=ASC&sort=current_severity`;
    }

    return (
        <ResourceContextProvider value="branches">
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        bulkActionButtons={false}
                        rowClick={false}
                    >
                        <WithRecord
                            label="Name"
                            render={(branch) => (
                                <TextUrlField
                                    label="Name"
                                    text={branch.name}
                                    url={get_observations_url(product.id, branch.id)}
                                />
                            )}
                        />
                        <BooleanField source="is_default_branch" label="Default branch / version" sortable={false} />
                        {product?.has_branch_purls && <TextField source="purl" label="PURL" />}
                        {product?.has_branch_cpe23s && <TextField source="cpe23" label="CPE 2.3" />}
                        <WithRecord
                            label="Protect"
                            render={(branch) =>
                                !branch.is_default_branch && <BooleanField source="housekeeping_protect" />
                            }
                        />
                        {product?.has_branch_osv_linux_distribution && (
                            <WithRecord
                                label="OSV Linux dist."
                                render={(branch) => (
                                    <OSVLinuxDistributionField
                                        osv_linux_distribution={branch.osv_linux_distribution}
                                        osv_linux_release={branch.osv_linux_release}
                                        label="OSV Linux dist."
                                    />
                                )}
                            />
                        )}
                        <ObservationsCountField label="Open observations" withLabel={false} />
                        {feature_license_management() && product?.has_licenses && (
                            <LicensesCountField label="Licenses / Components" withLabel={false} />
                        )}
                        <DateField source="last_import" showTime />
                        <WithRecord
                            render={(branch) => (
                                <Stack direction="row" spacing={4}>
                                    {product?.permissions.includes(PERMISSION_BRANCH_EDIT) && (
                                        <BranchEdit product={product} />
                                    )}
                                    {product?.permissions.includes(PERMISSION_PRODUCT_EDIT) &&
                                        !branch.is_default_branch && <DefaultBranch branch={branch} />}
                                    {product?.permissions.includes(PERMISSION_BRANCH_DELETE) &&
                                        !branch.is_default_branch && <BranchDelete branch={branch} />}
                                </Stack>
                            )}
                        />
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default BranchEmbeddedList;
