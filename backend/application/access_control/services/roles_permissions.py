from enum import IntEnum


class Roles(IntEnum):
    Reader = 1
    Upload = 2
    Writer = 3
    Maintainer = 4
    Owner = 5

    @classmethod
    def has_value(cls, value):
        try:
            Roles(value)
            return True
        except ValueError:
            return False


class Permissions(IntEnum):
    Product_Group_View = 1001
    Product_Group_Edit = 1002
    Product_Group_Delete = 1003
    Product_Group_Create = 1004

    Product_View = 1101
    Product_Edit = 1102
    Product_Delete = 1103
    Product_Create = 1104
    Product_Import_Observations = 1105

    Product_Member_View = 1201
    Product_Member_Edit = 1202
    Product_Member_Delete = 1203
    Product_Member_Create = 1204

    Product_Rule_View = 1301
    Product_Rule_Edit = 1302
    Product_Rule_Delete = 1303
    Product_Rule_Create = 1304
    Product_Rule_Apply = 1305

    Branch_View = 1401
    Branch_Edit = 1402
    Branch_Delete = 1403
    Branch_Create = 1404

    Service_View = 1501
    Service_Delete = 1503

    Observation_View = 2001
    Observation_Edit = 2002
    Observation_Delete = 2003
    Observation_Create = 2004
    Observation_Assessment = 2005

    Api_Configuration_View = 3001
    Api_Configuration_Edit = 3002
    Api_Configuration_Delete = 3003
    Api_Configuration_Create = 3004

    Product_Api_Token_Revoke = 4003
    Product_Api_Token_Create = 4004

    VEX_View = 5001
    VEX_Edit = 5002
    VEX_Delete = 5003
    VEX_Create = 5004

    @classmethod
    def has_value(cls, value):
        try:
            Permissions(value)
            return True
        except ValueError:
            return False

    @classmethod
    def get_product_group_permissions(cls):
        return {
            Permissions.Product_Group_View,
            Permissions.Product_Group_Edit,
            Permissions.Product_Group_Delete,
            Permissions.Product_Group_Create,
        }

    @classmethod
    def get_observation_permissions(cls):
        return {
            Permissions.Observation_View,
            Permissions.Observation_Edit,
            Permissions.Observation_Delete,
            Permissions.Observation_Create,
            Permissions.Observation_Assessment,
        }

    @classmethod
    def get_product_member_permissions(cls):
        return {
            Permissions.Product_Member_View,
            Permissions.Product_Member_Edit,
            Permissions.Product_Member_Delete,
        }

    @classmethod
    def get_product_rule_permissions(cls):
        return {
            Permissions.Product_Rule_View,
            Permissions.Product_Rule_Edit,
            Permissions.Product_Rule_Delete,
            Permissions.Product_Rule_Create,
            Permissions.Product_Rule_Apply,
        }

    @classmethod
    def get_branch_permissions(cls):
        return {
            Permissions.Branch_View,
            Permissions.Branch_Edit,
            Permissions.Branch_Delete,
            Permissions.Branch_Create,
        }

    @classmethod
    def get_service_permissions(cls):
        return {
            Permissions.Service_View,
            Permissions.Service_Delete,
        }

    @classmethod
    def get_api_configuration_permissions(cls):
        return {
            Permissions.Api_Configuration_View,
            Permissions.Api_Configuration_Edit,
            Permissions.Api_Configuration_Delete,
            Permissions.Api_Configuration_Create,
        }

    @classmethod
    def get_vex_permissions(cls):
        return {
            Permissions.VEX_View,
            Permissions.VEX_Edit,
            Permissions.VEX_Delete,
            Permissions.VEX_Create,
        }

    @classmethod
    def get_vulnerability_check_permissions(cls):
        return {
            Permissions.Product_View,
        }


def get_roles_with_permissions():
    return {
        Roles.Reader: {
            Permissions.Product_Group_View,
            Permissions.Product_View,
            Permissions.Product_Member_View,
            Permissions.Product_Rule_View,
            Permissions.Branch_View,
            Permissions.Service_View,
            Permissions.Observation_View,
            Permissions.Api_Configuration_View,
            Permissions.VEX_View,
        },
        Roles.Upload: {
            Permissions.Product_Import_Observations,
        },
        Roles.Writer: {
            Permissions.Product_Group_View,
            Permissions.Product_View,
            Permissions.Product_Import_Observations,
            Permissions.Product_Member_View,
            Permissions.Product_Rule_View,
            Permissions.Branch_View,
            Permissions.Service_View,
            Permissions.Observation_View,
            Permissions.Observation_Edit,
            Permissions.Observation_Create,
            Permissions.Observation_Assessment,
            Permissions.Api_Configuration_View,
            Permissions.VEX_View,
        },
        Roles.Maintainer: {
            Permissions.Product_Group_View,
            Permissions.Product_Group_Edit,
            Permissions.Product_View,
            Permissions.Product_Edit,
            Permissions.Product_Import_Observations,
            Permissions.Product_Member_View,
            Permissions.Product_Member_Edit,
            Permissions.Product_Member_Delete,
            Permissions.Product_Member_Create,
            Permissions.Product_Rule_View,
            Permissions.Product_Rule_Edit,
            Permissions.Product_Rule_Delete,
            Permissions.Product_Rule_Create,
            Permissions.Product_Rule_Apply,
            Permissions.Branch_View,
            Permissions.Branch_Edit,
            Permissions.Branch_Delete,
            Permissions.Branch_Create,
            Permissions.Service_View,
            Permissions.Service_Delete,
            Permissions.Observation_View,
            Permissions.Observation_Edit,
            Permissions.Observation_Create,
            Permissions.Observation_Assessment,
            Permissions.Api_Configuration_View,
            Permissions.Api_Configuration_Edit,
            Permissions.Api_Configuration_Delete,
            Permissions.Api_Configuration_Create,
            Permissions.VEX_View,
            Permissions.VEX_Edit,
            Permissions.VEX_Create,
            Permissions.VEX_Delete,
        },
        Roles.Owner: {
            Permissions.Product_Group_View,
            Permissions.Product_Group_Edit,
            Permissions.Product_Group_Delete,
            Permissions.Product_View,
            Permissions.Product_Edit,
            Permissions.Product_Delete,
            Permissions.Product_Import_Observations,
            Permissions.Product_Member_View,
            Permissions.Product_Member_Edit,
            Permissions.Product_Member_Delete,
            Permissions.Product_Member_Create,
            Permissions.Product_Rule_View,
            Permissions.Product_Rule_Edit,
            Permissions.Product_Rule_Delete,
            Permissions.Product_Rule_Create,
            Permissions.Product_Rule_Apply,
            Permissions.Branch_View,
            Permissions.Branch_Edit,
            Permissions.Branch_Delete,
            Permissions.Branch_Create,
            Permissions.Service_View,
            Permissions.Service_Delete,
            Permissions.Observation_View,
            Permissions.Observation_Edit,
            Permissions.Observation_Create,
            Permissions.Observation_Delete,
            Permissions.Observation_Assessment,
            Permissions.Api_Configuration_View,
            Permissions.Api_Configuration_Edit,
            Permissions.Api_Configuration_Delete,
            Permissions.Api_Configuration_Create,
            Permissions.Product_Api_Token_Revoke,
            Permissions.Product_Api_Token_Create,
            Permissions.VEX_View,
            Permissions.VEX_Edit,
            Permissions.VEX_Create,
            Permissions.VEX_Delete,
        },
    }


def get_permissions_for_role(role: int) -> list[Permissions]:
    return get_roles_with_permissions().get(role)
