from application.licenses.models import License_Group, License_Group_Member


def copy_license_group(source_license_group: License_Group, name: str) -> License_Group:
    new_license_group = License_Group.objects.create(
        name=name,
        description=source_license_group.description,
        is_public=source_license_group.is_public,
    )

    for license_to_be_added in source_license_group.licenses.all():
        new_license_group.licenses.add(license_to_be_added)

    members = License_Group_Member.objects.filter(license_group=source_license_group)
    for member in members:
        License_Group_Member.objects.update_or_create(
            license_group=new_license_group,
            user=member.user,
            is_manager=member.is_manager,
        )

    return new_license_group
