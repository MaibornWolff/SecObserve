from django_filters import CharFilter, FilterSet, OrderingFilter

from application.vex.models import CSAF, OpenVEX


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
            ("document_id", "document_id"),
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
            ("document_id", "document_id"),
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
