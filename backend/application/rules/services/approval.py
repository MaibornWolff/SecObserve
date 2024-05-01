from django.utils import timezone
from rest_framework.exceptions import ValidationError

from application.commons.services.global_request import get_current_user
from application.rules.models import Rule
from application.rules.types import Rule_Status


def rule_approval(rule: Rule, approval_status: str, approval_remark: str) -> None:
    if rule.approval_status != Rule_Status.RULE_STATUS_NEEDS_APPROVAL:
        raise ValidationError("Rule does not need approval")

    approval_user = get_current_user()
    if rule.user == approval_user:
        raise ValidationError("Users cannot approve the rules they created/modified")

    rule.approval_status = approval_status
    rule.approval_user = approval_user
    rule.approval_remark = approval_remark
    rule.approval_date = timezone.now()
    rule.save()
