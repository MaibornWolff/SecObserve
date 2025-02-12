from typing import Any

from django.core.validators import EMPTY_VALUES
from django.db.models import F, QuerySet
from django_filters import OrderingFilter


# Copied from https://github.com/carltongibson/django-filter/issues/274#issuecomment-1862859556
class ExtendedOrderingFilter(OrderingFilter):
    def filter(self, qs: QuerySet, value: Any) -> QuerySet:
        if value in EMPTY_VALUES:
            return qs

        ordering = []
        for param in value:
            fields = self.param_map[param.removeprefix("-")]
            if not isinstance(fields, tuple):
                fields = (fields,)
            for field in fields:
                if isinstance(field, str):
                    field = F(field)
                ordering.append(field.desc() if param.startswith("-") else field)

        return qs.order_by(*ordering)
