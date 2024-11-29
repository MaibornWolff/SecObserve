import ChecklistIcon from "@mui/icons-material/Checklist";
import {
    AutocompleteInput,
    Datagrid,
    DateField,
    FilterForm,
    ListContextProvider,
    ReferenceField,
    ReferenceInput,
    ResourceContextProvider,
    TextField,
    TextInput,
    useListController,
} from "react-admin";
import { Fragment } from "react/jsx-runtime";

import { CustomPagination } from "../../commons/custom_fields/CustomPagination";
import { feature_vex_enabled } from "../../commons/functions";
import ListHeader from "../../commons/layout/ListHeader";
import { AutocompleteInputMedium, AutocompleteInputWide } from "../../commons/layout/themes";
import { getSettingListSize } from "../../commons/user_settings/functions";
import { ASSESSMENT_STATUS_NEEDS_APPROVAL } from "../types";
import { OBSERVATION_SEVERITY_CHOICES, OBSERVATION_STATUS_CHOICES } from "../types";
import AssessmentBulkApproval from "./AssessmentBulkApproval";

const BulkActionButtons = () => (
    <Fragment>
        <AssessmentBulkApproval />
    </Fragment>
);

function listFilters(product_is_set: boolean) {
    const filters = [];
    if (!product_is_set) {
        filters.push(
            <ReferenceInput source="product" reference="products" sort={{ field: "name", order: "ASC" }} alwaysOn>
                <AutocompleteInputMedium optionText="name" />
            </ReferenceInput>,
            <ReferenceInput
                source="product_group"
                reference="product_groups"
                sort={{ field: "name", order: "ASC" }}
                alwaysOn
            >
                <AutocompleteInputMedium optionText="name" />
            </ReferenceInput>,
            <ReferenceInput source="branch" reference="branches" sort={{ field: "name", order: "ASC" }} alwaysOn>
                <AutocompleteInputWide optionText="name_with_product" label="Branch / Version" />
            </ReferenceInput>
        );
    }
    filters.push(
        <TextInput source="observation_title" label="Observation title" alwaysOn />,
        <ReferenceInput source="user" reference="users" sort={{ field: "full_name", order: "ASC" }} alwaysOn>
            <AutocompleteInputMedium optionText="full_name" />
        </ReferenceInput>,
        <AutocompleteInput source="severity" label="Severity" choices={OBSERVATION_SEVERITY_CHOICES} alwaysOn />,
        <AutocompleteInput source="status" label="Status" choices={OBSERVATION_STATUS_CHOICES} alwaysOn />,
        <TextInput source="origin_component_name_version" label="Component" alwaysOn />
    );
    return filters;
}

type ObservationLogApprovalListProps = {
    product: any;
};

const ObservationLogApprovalList = ({ product }: ObservationLogApprovalListProps) => {
    const listContext = useListController({
        filter: { product: product ? Number(product.id) : null, assessment_status: ASSESSMENT_STATUS_NEEDS_APPROVAL },
        perPage: 25,
        resource: "observation_logs",
        sort: { field: "created", order: "ASC" },
        disableSyncWithLocation: true,
        storeKey: "observation_logs.approval",
    });

    if (listContext.isLoading) {
        return <div>Loading...</div>;
    }

    if (listContext.data) {
        listContext.data.forEach((element: any) => {
            if (element.comment.length > 255) {
                element.comment_shortened = element.comment.substring(0, 255) + "...";
            } else {
                element.comment_shortened = element.comment;
            }
        });
    }

    const ShowObservationLogs = (id: any) => {
        return "../../../../observation_logs/" + id + "/show";
    };

    localStorage.setItem("observationlogapprovallist", "true");
    localStorage.removeItem("observationlogembeddedlist");
    return (
        <ResourceContextProvider value="observation_logs">
            <ListHeader icon={ChecklistIcon} title="Reviews" />
            <ListContextProvider value={listContext}>
                <div style={{ width: "100%" }}>
                    <FilterForm filters={listFilters(typeof product !== "undefined")} />
                    <Datagrid
                        size={getSettingListSize()}
                        sx={{ width: "100%" }}
                        bulkActionButtons={<BulkActionButtons />}
                        rowClick={ShowObservationLogs}
                        resource="observation_logs"
                    >
                        {!product && <TextField source="product_name" label="Product" />}
                        {!product && <TextField source="branch_name" label="Branch / Version" />}
                        {product && <TextField source="origin_component_name_version" label="Component" />}
                        <ReferenceField
                            source="observation"
                            reference="observations"
                            link="show"
                            sx={{ "& a": { textDecoration: "none" } }}
                        >
                            <TextField source="title" />
                        </ReferenceField>
                        <TextField source="user_full_name" label="User" />
                        <TextField source="severity" emptyText="---" />
                        <TextField source="status" emptyText="---" />
                        {feature_vex_enabled() && (
                            <TextField
                                label="VEX justification"
                                source="vex_justification"
                                emptyText="---"
                                sx={{ wordBreak: "break-word" }}
                            />
                        )}
                        <TextField
                            source="comment_shortened"
                            sortable={false}
                            label="Comment"
                            sx={{ wordBreak: "break-word" }}
                        />
                        <DateField source="created" showTime />
                    </Datagrid>
                    <CustomPagination />
                </div>
            </ListContextProvider>
        </ResourceContextProvider>
    );
};

export default ObservationLogApprovalList;
