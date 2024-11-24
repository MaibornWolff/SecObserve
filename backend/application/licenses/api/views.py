from dataclasses import dataclass
from typing import Optional

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.access_control.services.authorization import user_has_permission_or_403
from application.access_control.services.roles_permissions import Permissions
from application.core.models import Branch, Product
from application.core.queries.branch import get_branch_by_id
from application.core.queries.product import get_product_by_id
from application.licenses.api.filters import (
    LicenseComponentEvidenceFilter,
    LicenseComponentFilter,
    LicenseFilter,
    LicenseGroupAuthorizationGroupFilter,
    LicenseGroupFilter,
    LicenseGroupMemberFilter,
    LicensePolicyAuthorizationGroupFilter,
    LicensePolicyFilter,
    LicensePolicyItemFilter,
    LicensePolicyMemberFilter,
)
from application.licenses.api.permissions import (
    UserHasLicenseGroupAuthenticationGroupMemberPermission,
    UserHasLicenseGroupMemberPermission,
    UserHasLicenseGroupPermission,
    UserHasLicensePolicyAuthorizationGroupMemberPermission,
    UserHasLicensePolicyItemMemberPermission,
    UserHasLicensePolicyPermission,
)
from application.licenses.api.serializers import (
    LicenseComponentEvidenceSerializer,
    LicenseComponentIdSerializer,
    LicenseComponentListSerializer,
    LicenseComponentOverviewSerializer,
    LicenseComponentSerializer,
    LicenseGroupAuthorizationGroupMemberSerializer,
    LicenseGroupCopySerializer,
    LicenseGroupLicenseAddRemoveSerializer,
    LicenseGroupMemberSerializer,
    LicenseGroupSerializer,
    LicensePolicyAuthorizationGroupMemberSerializer,
    LicensePolicyCopySerializer,
    LicensePolicyItemSerializer,
    LicensePolicyMemberSerializer,
    LicensePolicySerializer,
    LicenseSerializer,
)
from application.licenses.models import (
    License,
    License_Component,
    License_Component_Evidence,
    License_Group,
    License_Group_Authorization_Group_Member,
    License_Group_Member,
    License_Policy,
    License_Policy_Authorization_Group_Member,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license import get_license
from application.licenses.queries.license_component import (
    get_license_component_licenses,
    get_license_components,
)
from application.licenses.queries.license_component_evidence import (
    get_license_component_evidences,
)
from application.licenses.queries.license_group import (
    get_license_group,
    get_license_groups,
)
from application.licenses.queries.license_group_authorization_group_member import (
    get_license_group_authorization_group_members,
)
from application.licenses.queries.license_group_member import (
    get_license_group_member,
    get_license_group_members,
)
from application.licenses.queries.license_policy import (
    get_license_policies,
    get_license_policy,
)
from application.licenses.queries.license_policy_authorization_group_member import (
    get_license_policy_authorization_group_members,
)
from application.licenses.queries.license_policy_item import get_license_policy_items
from application.licenses.queries.license_policy_member import (
    get_license_policy_member,
    get_license_policy_members,
)
from application.licenses.services.license_group import (
    copy_license_group,
    import_scancode_licensedb,
)
from application.licenses.services.license_policy import (
    apply_license_policy,
    copy_license_policy,
)


@dataclass
class LicenseComponentOverviewElement:
    branch_name: Optional[str]
    spdx_id: Optional[str]
    license_name: Optional[str]
    unknown_license: Optional[str]
    evaluation_result: str
    num_components: int


@dataclass
class LicenseComponentOverview:
    count: int
    results: list[LicenseComponentOverviewElement]


class LicenseComponentViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseComponentSerializer
    filterset_class = LicenseComponentFilter
    queryset = License_Component.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "list":
            return LicenseComponentListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return (
            get_license_components().select_related("branch").select_related("license")
        )

    @extend_schema(
        methods=["GET"],
        responses={200: LicenseComponentOverviewSerializer},
        parameters=[
            OpenApiParameter(name="product", type=int, required=True),
            OpenApiParameter(name="branch", type=int),
        ],
    )
    @action(detail=False, methods=["get"])
    def license_overview(self, request):
        product_id = request.query_params.get("product")
        if not product_id:
            raise ValidationError("No product id provided")
        product = self.__get_product(product_id)
        branch = self.__get_branch(product, request.query_params.get("branch"))
        spdx_id = request.query_params.get("spdx_id")
        unknown_license = request.query_params.get("unknown_license")
        evaluation_result = request.query_params.get("evaluation_result")
        purl_type = request.query_params.get("purl_type")

        license_overview_elements = get_license_component_licenses(product, branch)
        if spdx_id:
            license_overview_elements = license_overview_elements.filter(
                license__spdx_id__icontains=spdx_id
            )
        if unknown_license:
            license_overview_elements = license_overview_elements.filter(
                unknown_license__icontains=unknown_license
            )
        if evaluation_result:
            license_overview_elements = license_overview_elements.filter(
                evaluation_result=evaluation_result
            )
        if purl_type:
            license_overview_elements = license_overview_elements.filter(
                purl_type=purl_type
            )

        results = []
        for element in license_overview_elements:
            license_component_overview_element = LicenseComponentOverviewElement(
                branch_name=element["branch__name"],
                spdx_id=element["license__spdx_id"],
                license_name=element["license__name"],
                unknown_license=element["unknown_license"],
                evaluation_result=element["evaluation_result"],
                num_components=element["id__count"],
            )
            results.append(license_component_overview_element)

        license_overview = LicenseComponentOverview(
            count=len(results),
            results=results,
        )

        response_serializer = LicenseComponentOverviewSerializer(license_overview)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def __get_product(self, pk: int) -> Product:
        if not pk:
            raise ValidationError("No product id provided")

        product = get_product_by_id(pk)
        if not product:
            raise NotFound()

        user_has_permission_or_403(product, Permissions.Product_View)

        return product

    def __get_branch(self, product: Product, pk: int) -> Optional[Branch]:
        if not pk:
            return None

        branch = get_branch_by_id(product, pk)
        if not branch:
            raise NotFound()

        user_has_permission_or_403(branch, Permissions.Branch_View)

        return branch


class LicenseComponentIdViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseComponentIdSerializer
    filterset_class = LicenseComponentFilter
    queryset = License_Component.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_license_components()


class LicenseComponentEvidenceViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin
):
    serializer_class = LicenseComponentEvidenceSerializer
    filterset_class = LicenseComponentEvidenceFilter
    queryset = License_Component_Evidence.objects.none()

    def get_queryset(self):
        return get_license_component_evidences().select_related(
            "license_component__product"
        )


class LicenseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilter
    queryset = License.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["spdx_id", "name"]


class LicenseGroupViewSet(ModelViewSet):
    serializer_class = LicenseGroupSerializer
    filterset_class = LicenseGroupFilter
    queryset = License_Group.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    permission_classes = [IsAuthenticated, UserHasLicenseGroupPermission]

    def get_queryset(self):
        return get_license_groups()

    @extend_schema(
        methods=["POST"],
        request=LicenseGroupCopySerializer,
        responses={HTTP_201_CREATED: LicenseGroupSerializer},
    )
    @action(detail=True, methods=["post"])
    def copy(self, request, pk):
        user = request.user
        if user.is_external:
            raise PermissionDenied("You are not allowed to copy a license group")

        request_serializer = LicenseGroupCopySerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_group = get_license_group(pk)
        if license_group is None:
            raise NotFound("License group not found")

        if not (user.is_superuser or license_group.is_public):
            license_group_member = get_license_group_member(license_group, user)
            if not license_group_member:
                raise NotFound("License group not found")

        name = request_serializer.validated_data.get("name")
        try:
            License_Group.objects.get(name=name)
            raise ValidationError("License group with this name already exists")
        except License_Group.DoesNotExist:
            pass

        new_license_group = copy_license_group(license_group, name)

        return Response(
            status=HTTP_201_CREATED,
            data=LicenseGroupSerializer(new_license_group).data,
        )

    @extend_schema(
        methods=["POST"],
        request=LicenseGroupLicenseAddRemoveSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def add_license(self, request, pk):
        request_serializer = LicenseGroupLicenseAddRemoveSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_group = get_license_group(pk)
        if license_group is None:
            raise NotFound("License group not found")

        user = request.user
        if not user.is_superuser:
            license_group_member = get_license_group_member(license_group, user)
            if not license_group_member:
                raise NotFound("License group not found")
            if not license_group_member.is_manager:
                raise PermissionDenied("User is not a manager of this license group")

        license_id = request_serializer.validated_data.get("license")
        license_to_be_added = get_license(license_id)
        if not license_to_be_added:
            raise ValidationError(f"License {license_id} not found")

        if license_to_be_added in license_group.licenses.filter(id=license_id):
            raise ValidationError(
                f"License {license_to_be_added} is already in this license group"
            )

        license_group.licenses.add(license_to_be_added)

        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=LicenseGroupLicenseAddRemoveSerializer,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def remove_license(self, request, pk):
        request_serializer = LicenseGroupLicenseAddRemoveSerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_group = get_license_group(pk)
        if license_group is None:
            raise NotFound("License group not found")

        user = request.user
        if not user.is_superuser:
            license_group_member = get_license_group_member(license_group, user)
            if not license_group_member:
                raise NotFound("License group not found")
            if not license_group_member.is_manager:
                raise PermissionDenied("User is not a manager of this license group")

        license_id = request_serializer.validated_data.get("license")
        license_to_be_removed = get_license(license_id)
        if not license_to_be_removed:
            raise ValidationError(f"License {license_id} not found")

        license_group.licenses.remove(license_to_be_removed)

        return Response(status=HTTP_204_NO_CONTENT)

    @extend_schema(
        methods=["POST"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=False, methods=["post"])
    def import_scancode_licensedb(self, request):
        user = request.user
        if not user.is_superuser:
            raise PermissionDenied(
                "User is not allowed to import license groups from ScanCode LicenseDB"
            )

        import_scancode_licensedb()

        return Response(status=HTTP_204_NO_CONTENT)


class LicenseGroupMemberViewSet(ModelViewSet):
    serializer_class = LicenseGroupMemberSerializer
    filterset_class = LicenseGroupMemberFilter
    queryset = License_Group_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicenseGroupMemberPermission]

    def get_queryset(self):
        return (
            get_license_group_members()
            .select_related("license_group")
            .select_related("user")
        )


class LicenseGroupAuthorizationGroupMemberViewSet(ModelViewSet):
    serializer_class = LicenseGroupAuthorizationGroupMemberSerializer
    filterset_class = LicenseGroupAuthorizationGroupFilter
    queryset = License_Group_Authorization_Group_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [
        IsAuthenticated,
        UserHasLicenseGroupAuthenticationGroupMemberPermission,
    ]

    def get_queryset(self):
        return (
            get_license_group_authorization_group_members()
            .select_related("license_group")
            .select_related("authorization_group")
        )


class LicensePolicyViewSet(ModelViewSet):
    serializer_class = LicensePolicySerializer
    filterset_class = LicensePolicyFilter
    queryset = License_Policy.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyPermission]

    def get_queryset(self):
        return get_license_policies()

    @extend_schema(
        methods=["POST"],
        request=LicensePolicyCopySerializer,
        responses={HTTP_201_CREATED: LicensePolicySerializer},
    )
    @action(detail=True, methods=["post"])
    def copy(self, request, pk):
        user = request.user
        if user.is_external:
            raise PermissionDenied("You are not allowed to copy a license policy")

        request_serializer = LicensePolicyCopySerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_policy = get_license_policy(pk)
        if license_policy is None:
            raise NotFound("License policy not found")

        if not (user.is_superuser or license_policy.is_public):
            license_policy_member = get_license_policy_member(license_policy, user)
            if not license_policy_member:
                raise NotFound("License policy not found")

        name = request_serializer.validated_data.get("name")
        try:
            License_Policy.objects.get(name=name)
            raise ValidationError("License policy with this name already exists")
        except License_Policy.DoesNotExist:
            pass

        new_license_policy = copy_license_policy(license_policy, name)

        return Response(
            status=HTTP_201_CREATED,
            data=LicensePolicySerializer(new_license_policy).data,
        )

    @extend_schema(
        methods=["POST"],
        request=None,
        responses={HTTP_204_NO_CONTENT: None},
    )
    @action(detail=True, methods=["post"])
    def apply(self, request, pk):
        license_policy = get_license_policy(pk)
        if license_policy is None:
            raise NotFound("License policy not found")

        user = request.user
        if not user.is_superuser:
            license_policy_member = get_license_policy_member(license_policy, user)
            if not license_policy.is_public and not license_policy_member:
                raise NotFound("License policy not found")
            if license_policy_member and not license_policy_member.is_manager:
                raise PermissionDenied("You are not allowed to apply a license policy")

        apply_license_policy(license_policy)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )


class LicensePolicyItemViewSet(ModelViewSet):
    serializer_class = LicensePolicyItemSerializer
    filterset_class = LicensePolicyItemFilter
    queryset = License_Policy_Item.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyItemMemberPermission]

    def get_queryset(self):
        return (
            get_license_policy_items()
            .select_related("license_policy")
            .select_related("license")
            .select_related("license_group")
        )


class LicensePolicyMemberViewSet(ModelViewSet):
    serializer_class = LicensePolicyMemberSerializer
    filterset_class = LicensePolicyMemberFilter
    queryset = License_Policy_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyItemMemberPermission]

    def get_queryset(self):
        return (
            get_license_policy_members()
            .select_related("license_policy")
            .select_related("user")
        )


class LicensePolicyAuthorizationGroupMemberViewSet(ModelViewSet):
    serializer_class = LicensePolicyAuthorizationGroupMemberSerializer
    filterset_class = LicensePolicyAuthorizationGroupFilter
    queryset = License_Policy_Authorization_Group_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [
        IsAuthenticated,
        UserHasLicensePolicyAuthorizationGroupMemberPermission,
    ]

    def get_queryset(self):
        return (
            get_license_policy_authorization_group_members()
            .select_related("license_policy")
            .select_related("authorization_group")
        )
