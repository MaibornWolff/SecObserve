from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from application.licenses.api.filters import (
    LicenseComponentFilter,
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
    LicenseComponentSerializer,
    LicenseGroupCopySerializer,
    LicenseGroupLicenseAddRemoveSerializer,
    LicenseGroupMemberSerializer,
    LicenseGroupSerializer,
    LicensePolicyCopySerializer,
    LicensePolicyItemSerializer,
    LicensePolicyMemberSerializer,
    LicensePolicySerializer,
    LicenseSerializer,
)
from application.licenses.models import (
    License,
    License_Component,
    License_Group,
    License_Group_Member,
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)
from application.licenses.queries.license import get_license
from application.licenses.queries.license_component import get_license_components
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
from application.licenses.services.license_group import copy_license_group
from application.licenses.services.license_policy import (
    apply_license_policy,
    copy_license_policy,
)


class LicenseComponentViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseComponentSerializer
    filterset_class = LicenseComponentFilter
    queryset = License_Component.objects.none()
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return get_license_components()


class LicenseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = LicenseSerializer
    filterset_class = LicenseFilter
    queryset = License.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["spdx_id"]


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
                raise PermissionDenied("User is not a manager of the license group")

        license_id = request_serializer.validated_data.get("license")
        license_to_be_added = get_license(license_id)
        if not license_to_be_added:
            raise ValidationError(f"License {license_id} not found")

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
                raise PermissionDenied("User is not a manager of the license group")

        license_id = request_serializer.validated_data.get("license")
        license_to_be_removed = get_license(license_id)
        if not license_to_be_removed:
            raise ValidationError(f"License {license_id} not found")

        license_group.licenses.remove(license_to_be_removed)

        return Response(status=HTTP_204_NO_CONTENT)


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
        if not (user.is_superuser or license_policy.is_public):
            license_policy_member = get_license_policy_member(license_policy, user)
            if not license_policy_member:
                raise NotFound("License policy not found")

        if not (user.is_superuser or license_policy_member.is_manager):
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
        return get_license_policy_items()


class LicensePolicyMemberViewSet(ModelViewSet):
    serializer_class = LicensePolicyMemberSerializer
    filterset_class = LicensePolicyMemberFilter
    queryset = License_Policy_Member.objects.none()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated, UserHasLicensePolicyItemMemberPermission]

    def get_queryset(self):
        return get_license_policy_members()
