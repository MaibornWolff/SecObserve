from django_filters import CharFilter, FilterSet, OrderingFilter

from application.vex.models import (
    CSAF,
    CSAF_Branch,
    CSAF_Vulnerability,
    OpenVEX,
    OpenVEX_Branch,
    OpenVEX_Vulnerability,
    VEX_Counter,
)


class CSAFFilter(FilterSet):
    vulnerability_names__name = CharFilter(
        field_name="vulnerability_names__name", lookup_expr="icontains", distinct=True
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_full_name"),
            ("product__name", "product_name"),
            ("document_id_prefix", "document_id_prefix"),
            ("document_base_id", "document_base_id"),
            ("version", "version"),
            ("content_hash", "content_hash"),
            ("title", "title"),
            ("tlp_label", "tlp_label"),
            ("tracking_initial_release_date", "tracking_initial_release_date"),
            ("tracking_current_release_date", "tracking_current_release_date"),
            ("tracking_status", "tracking_status"),
            ("publisher_name", "publisher_name"),
            ("publisher_category", "publisher_category"),
            ("publisher_namespace", "publisher_namespace"),
        ),
    )

    class Meta:
        model = CSAF
        fields = [
            "product",
            "vulnerability_names__name",
            "document_id_prefix",
            "title",
            "publisher_name",
        ]


class CSAFVulnerabilityFilter(FilterSet):
    class Meta:
        model = CSAF_Vulnerability
        fields = [
            "csaf",
            "name",
        ]


class CSAFBranchFilter(FilterSet):
    class Meta:
        model = CSAF_Branch
        fields = [
            "csaf",
            "branch__name",
        ]


class OpenVEXFilter(FilterSet):
    vulnerability_names__name = CharFilter(
        field_name="vulnerability_names__name", lookup_expr="icontains", distinct=True
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("user__full_name", "user_full_name"),
            ("product__name", "product_name"),
            ("document_id_prefix", "document_id_prefix"),
            ("document_base_id", "document_base_id"),
            ("version", "version"),
            ("content_hash", "content_hash"),
            ("author", "author"),
            ("role", "role"),
            ("timestamp", "timestamp"),
            ("last_updated", "last_updated"),
        ),
    )

    class Meta:
        model = OpenVEX
        fields = [
            "product",
            "vulnerability_names__name",
            "document_id_prefix",
            "author",
        ]


class OpenVEXVulnerabilityFilter(FilterSet):
    class Meta:
        model = OpenVEX_Vulnerability
        fields = [
            "openvex",
            "name",
        ]


class OpenVEXBranchFilter(FilterSet):
    class Meta:
        model = OpenVEX_Branch
        fields = [
            "openvex",
            "branch__name",
        ]


class VEXCounterFilter(FilterSet):
    document_id_prefix = CharFilter(
        field_name="document_id_prefix", lookup_expr="icontains", distinct=True
    )

    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("document_id_prefix", "document_id_prefix"),
            ("year", "year"),
        ),
    )

    class Meta:
        model = VEX_Counter
        fields = [
            "document_id_prefix",
            "year",
        ]
