import { Paper, Stack } from "@mui/material";
import {
    BooleanField,
    Datagrid,
    ListContextProvider,
    Pagination,
    TextField,
    WithRecord,
    useListController,
} from "react-admin";

import { PERMISSION_BRANCH_DELETE, PERMISSION_BRANCH_EDIT } from "../../access_control/types";
import ObservationsCountField from "../../commons/custom_fields/ObservationsCountField";
import BranchDelete from "./BranchDelete";
import BranchEdit from "./BranchEdit";

type BranchEmbeddedListProps = {
    product: any;
};

const BranchEmbeddedList = ({ product }: BranchEmbeddedListProps) => {
    const filter = { product: Number(product.id) };
    const perPage = 25;
    const resource = "branches";
    const sort = { field: "name", order: "ASC" };
    const disableSyncWithLocation = true;
    const storeKey = "branch.embedded";

    const listContext = useListController({
        filter,
        perPage,
        resource,
        sort,
        disableSyncWithLocation,
        storeKey,
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data === undefined) {
        listContext.data = [];
    }

    return (
        <ListContextProvider value={listContext}>
            <div style={{ width: "100%" }}>
                <Paper>
                    <Datagrid size="medium" sx={{ width: "100%" }} bulkActionButtons={false}>
                        <TextField source="name" />
                        <BooleanField source="is_default_branch" label="Default branch" />
                        <ObservationsCountField withLabel={false} />
                        <WithRecord
                            render={(branch) => (
                                <Stack direction="row" spacing={4}>
                                    {product && product.permissions.includes(PERMISSION_BRANCH_EDIT) && <BranchEdit />}
                                    {product && product.permissions.includes(PERMISSION_BRANCH_DELETE) && (
                                        <BranchDelete branch={branch} />
                                    )}
                                </Stack>
                            )}
                        />
                    </Datagrid>
                </Paper>
                <Pagination />
            </div>
        </ListContextProvider>
    );
};

export default BranchEmbeddedList;
