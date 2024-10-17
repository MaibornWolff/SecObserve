from application.licenses.models import (
    License_Policy,
    License_Policy_Item,
    License_Policy_Member,
)


def copy_license_policy(
    source_license_policy: License_Policy, name: str
) -> License_Policy:
    new_license_policy = License_Policy.objects.create(
        name=name,
        description=source_license_policy.description,
    )

    items = License_Policy_Item.objects.filter(license_policy=source_license_policy)
    for item in items:
        License_Policy_Item.objects.create(
            license_policy=new_license_policy,
            license_group=item.license_group,
            license=item.license,
            unknown_license=item.unknown_license,
            evaluation_result=item.evaluation_result,
        )

    members = License_Policy_Member.objects.filter(license_policy=source_license_policy)
    for member in members:
        License_Policy_Member.objects.create(
            license_policy=new_license_policy,
            user=member.user,
            is_manager=member.is_manager,
        )

    return new_license_policy
