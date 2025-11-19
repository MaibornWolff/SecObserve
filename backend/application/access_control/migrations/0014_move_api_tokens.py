import logging

from django.core.paginator import Paginator
from django.db import migrations

logger = logging.getLogger("secobserve.migration")


def copy_api_tokens(apps, schema_editor):
    API_Token_Legacy = apps.get_model("access_control", "API_Token")
    API_Token_Multiple = apps.get_model("access_control", "API_Token_Multiple")
    legacy_api_tokens = API_Token_Legacy.objects.all().order_by("pk")

    paginator = Paginator(legacy_api_tokens, 1000)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        creates = []

        for legacy_api_token in page.object_list:
            creates.append(
                API_Token_Multiple(
                    user=legacy_api_token.user,
                    name=legacy_api_token.name if hasattr(legacy_api_token, "name") else "default",
                    api_token_hash=legacy_api_token.api_token_hash,
                    expiration_date=(
                        legacy_api_token.expiration_date if hasattr(legacy_api_token, "expiration_date") else None
                    ),
                )
            )

        API_Token_Multiple.objects.bulk_create(creates)

    API_Token_Legacy.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "access_control",
            "0013_api_token_multiple",
        ),
    ]

    operations = [
        migrations.RunPython(
            copy_api_tokens,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
