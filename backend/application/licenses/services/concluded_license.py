from application.access_control.services.current_user import get_current_user
from application.licenses.models import Concluded_License, License_Component
from application.licenses.types import NO_LICENSE_INFORMATION


def apply_concluded_license(component: License_Component) -> None:
    concluded_license = None
    try:
        concluded_license = Concluded_License.objects.get(
            product=component.product,
            component_purl_type=component.component_purl_type,
            component_name=component.component_name,
            component_version=component.component_version,
        )
        concluded_comment = f"Set manually by {str(concluded_license.user)}"
    except Concluded_License.DoesNotExist:
        concluded_license = (
            Concluded_License.objects.filter(
                product=component.product,
                component_purl_type=component.component_purl_type,
                component_name=component.component_name,
            )
            .order_by("-last_updated")
            .first()
        )
        if concluded_license:
            concluded_comment = (
                f"Copied from version {concluded_license.component_version}, set by {str(concluded_license.user)}"
            )

    if concluded_license:
        if (
            concluded_license.concluded_spdx_license
            and component.effective_spdx_license != concluded_license.concluded_spdx_license
        ):
            component.concluded_spdx_license = concluded_license.concluded_spdx_license
            component.concluded_license_name = concluded_license.concluded_spdx_license.spdx_id
            component.concluded_comment = concluded_comment
        elif (
            concluded_license.concluded_license_expression
            and component.effective_license_expression != concluded_license.concluded_license_expression
        ):
            component.concluded_license_expression = concluded_license.concluded_license_expression
            component.concluded_license_name = concluded_license.concluded_license_expression
            component.concluded_comment = concluded_comment
        elif (
            concluded_license.concluded_non_spdx_license
            and component.effective_non_spdx_license != concluded_license.concluded_non_spdx_license
        ):
            component.concluded_non_spdx_license = concluded_license.concluded_non_spdx_license
            component.concluded_license_name = concluded_license.concluded_non_spdx_license
            component.concluded_comment = concluded_comment


def update_concluded_license(component: License_Component) -> None:
    if component.concluded_license_name == NO_LICENSE_INFORMATION:
        try:
            concluded_license = Concluded_License.objects.get(
                product=component.product,
                component_purl_type=component.component_purl_type,
                component_name=component.component_name,
                component_version=component.component_version,
            )
            concluded_license.delete()
        except Concluded_License.DoesNotExist:
            pass
    else:
        concluded_license, _ = Concluded_License.objects.update_or_create(
            product=component.product,
            component_purl_type=component.component_purl_type,
            component_name=component.component_name,
            component_version=component.component_version,
            defaults={
                "concluded_spdx_license": component.concluded_spdx_license,
                "concluded_license_expression": component.concluded_license_expression,
                "concluded_non_spdx_license": component.concluded_non_spdx_license,
                "user": get_current_user(),
            },
        )
        component.concluded_comment = f"Set manually by {str(concluded_license.user)}"
