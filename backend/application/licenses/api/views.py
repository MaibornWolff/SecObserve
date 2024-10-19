from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.licenses.api.filters import (
    ComponentFilter,
    ComponentLicenseFilter,
    LicenseFilter,
    LicenseGroupFilter,
    LicenseGroupMemberFilter,
    LicensePolicyFilter,
    LicensePolicyItemFilter,
    LicensePolicyMemberFilter,
)
from application.licenses.api.permissions import (
    UserHasLicenseGroupMemberPermission,
    UserHasLicenseGroupPermission,
    UserHasLicensePolicyItemMemberPermission,
    UserHasLicensePolicyPermission,
)
from application.licenses.api.serializers import (
    ComponentLicenseSerializer,
    ComponentSerializer,
    LicenseGroupCopySerializer,
    LicenseGroupMemberSerializer,
    LicenseGroupSerializer,
    LicensePolicyCopySerializer,
    LicensePolicyItemSerializer,
    LicensePolicyMemberSerializer,
    LicensePolicySerializer,
    LicenseSerializer,
)
from application.licenses.models import (
    Component,
    Component_License,
    License,
    License_Group,
    License_Group_Member,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.component import get_components
from application.licenses.queries.component_license import get_component_licenses
from application.licenses.queries.license_group import (
    get_license_group,
    get_license_groups,
)
from application.licenses.queries.license_group_member import (
    get_license_group_member,
    get_license_group_members,
)
from application.licenses.queries.license_policy import (
    get_license_policies,
    get_license_policy,
)
from application.licenses.queries.license_policy_item import get_license_policy_items
from application.licenses.queries.license_policy_member import (
    get_license_policy_member,
    get_license_policy_members,
)
from application.licenses.services.license_groups import copy_license_group
from application.licenses.services.license_policies import copy_license_policy


class ComponentLicenseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = ComponentLicenseSerializer
    filterset_class = ComponentLicenseFilter
    queryset = Component_License.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_component_licenses()


class ComponentViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = ComponentSerializer
    filterset_class = ComponentFilter
    queryset = Component.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_components()


class LicenseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilter
    queryset = License.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]


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
    @action(detail=False, methods=["post"])
    def copy(self, request, pk=None):
        request_serializer = LicenseGroupCopySerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_group_id = request_serializer.validated_data.get("license_group")
        license_group = get_license_group(license_group_id)
        if license_group is None:
            raise NotFound("License group not found")

        user = request.user
        if not user.is_superuser:
            license_policy_member = get_license_group_member(license_group, user)
            if not license_policy_member:
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


class LicenseGroupMemberViewSet(ModelViewSet):
    serializer_class = LicenseGroupMemberSerializer
    filterset_class = LicenseGroupMemberFilter
    queryset = License_Group_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicenseGroupMemberPermission]

    def get_queryset(self):
        return get_license_group_members()


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
    @action(detail=False, methods=["post"])
    def copy(self, request, pk=None):
        request_serializer = LicensePolicyCopySerializer(data=request.data)
        if not request_serializer.is_valid():
            raise ValidationError(request_serializer.errors)

        license_policy_id = request_serializer.validated_data.get("license_policy")
        license_policy = get_license_policy(license_policy_id)
        if license_policy is None:
            raise NotFound("License policy not found")

        user = request.user
        if not user.is_superuser:
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


class LicensePolicyItemViewSet(ModelViewSet):
    serializer_class = LicensePolicyItemSerializer
    filterset_class = LicensePolicyItemFilter
    queryset = License_Policy_Item.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyItemMemberPermission]

    def get_queryset(self):
        return get_license_policy_items()


class LicensePolicyMemberViewSet(ModelViewSet):
    serializer_class = LicensePolicyMemberSerializer
    filterset_class = LicensePolicyMemberFilter
    queryset = License_Policy_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyItemMemberPermission]

    def get_queryset(self):
        return get_license_policy_members()
