from django.db.models.signals import post_save
from django.dispatch import receiver

from application.commons.services.global_request import get_current_user
from application.licenses.models import License_Policy, License_Policy_Member


@receiver(post_save, sender=License_Policy)
def license_policy_post_save(  # pylint: disable=unused-argument
    sender, instance: License_Policy, created: bool, **kwargs
) -> None:
    # sender is needed according to Django documentation
    if created:
        user = get_current_user()
        if user and not user.is_superuser:
            License_Policy_Member.objects.create(
                license_policy=instance, user=user, is_manager=True
            )
