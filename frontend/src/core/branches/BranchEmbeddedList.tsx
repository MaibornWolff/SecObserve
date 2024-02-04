import { Stack } from "@mui/material";
import { BooleanField, Datagrid, DateField, ListContextProvider, WithRecord, useListController } from "react-admin";

import { PERMISSION_BRANCH_DELETE, PERMISSION_BRANCH_EDIT } from "../../access_control/types";
import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import TextUrlField from "../../commons/custom_fields/TextUrlField";
import { getSettingListSize } from "../../commons/settings/functions";
import BranchDelete from "./BranchDelete";
import BranchEdit from "./BranchEdit";

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

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    function get_observations_url(product_id: number, branch_id: number): string {
        return `#/products/${product_id}/show?displayedFilters=%7B%7D&filter=%7B%22current_status%22%3A%22Open%22%2C%22branch%22%3A${branch_id}%7D&order=ASC&sort=current_severity`;
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Datagrid size={getSettingListSize()} sx={{ width: "100%" }} bulkActionButtons={false}>
                    <WithRecord
                        label="Name"
                        render={(branch) => (
                            <TextUrlField text={branch.name} url={get_observations_url(product.id, branch.id)} />
                        )}
                    />
                    <BooleanField source="is_default_branch" label="Default branch" sortable={false} />
                    <ObservationsCountField withLabel={false} />
                    <DateField source="last_import" showTime />
                    <WithRecord
                        label="Protect"
                        render={(branch) => !branch.is_default_branch && <BooleanField source="housekeeping_protect" />}
                    />
                    <WithRecord
                        render={(branch) => (
                            <Stack direction="row" spacing={4}>
                                {product && product.permissions.includes(PERMISSION_BRANCH_EDIT) && <BranchEdit />}
                                {product &&
                                    product.permissions.includes(PERMISSION_BRANCH_DELETE) &&
                                    !branch.is_default_branch && <BranchDelete branch={branch} />}
                            </Stack>
                        )}
                    />
                </Datagrid>
                <CustomPagination />
            </div>
        </ListContextProvider>
    );
};

export default BranchEmbeddedList;
