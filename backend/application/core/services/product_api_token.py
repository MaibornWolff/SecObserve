from dataclasses import dataclass
from datetime import date
from typing import Optional

from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token_Multiple, User
from application.access_control.queries.user import get_user_by_username
from application.access_control.services.user_api_token import generate_api_token_hash
from application.authorization.services.roles_permissions import Roles
from application.core.models import Product, Product_Member
from application.core.queries.product_member import get_product_member


def create_product_api_token(product: Product, role: Roles, name: str, expiration_date: Optional[date]) -> str:
    product_user_name = _get_product_user_name(product, name)
    user = get_user_by_username(product_user_name)
    if user:
        try:
            API_Token_Multiple.objects.get(user=user)
            raise ValidationError("API token with this name already exists.")
        except API_Token_Multiple.DoesNotExist:
            pass

    api_token, api_token_hash = generate_api_token_hash()

    if user:
        user.is_active = True
    else:
        user = User(username=product_user_name, is_active=True)
    user.set_unusable_password()
    user.save()

    Product_Member(product=product, user=user, role=role).save()
    API_Token_Multiple(user=user, api_token_hash=api_token_hash, name=name, expiration_date=expiration_date).save()

    return api_token


def revoke_product_api_token(product: Product, api_token: API_Token_Multiple) -> None:
    user = api_token.user
    api_token.delete()

    product_member = get_product_member(product, user)
    if product_member:
        product_member.delete()

    user.is_active = False
    user.save()


@dataclass
class ProductAPIToken:
    id: int
    product: int
    role: int
    name: str
    expiration_date: Optional[date]


def get_product_api_tokens(product: Product) -> list[ProductAPIToken]:
    users = User.objects.filter(username__startswith=f"-product-{product.pk}-")
    if not users:
        return []

    product_api_tokens = []
    for user in users:
        product_member = get_product_member(product, user)
        if product_member:
            try:
                api_token = API_Token_Multiple.objects.get(user=user)
                product_api_tokens.append(
                    ProductAPIToken(
                        id=api_token.pk,
                        product=product.pk,
                        role=product_member.role,
                        name=api_token.name,
                        expiration_date=api_token.expiration_date,
                    )
                )
            except API_Token_Multiple.DoesNotExist:
                continue
            except API_Token_Multiple.MultipleObjectsReturned:
                continue

    return product_api_tokens


def _get_product_user_name(product: Product, name: str) -> str:
    return f"-product-{product.pk}-{name}-api_token-"
