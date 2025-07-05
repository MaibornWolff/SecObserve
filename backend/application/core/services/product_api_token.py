from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

from application.access_control.models import API_Token, User
from application.access_control.queries.user import get_user_by_username
from application.access_control.services.roles_permissions import Roles
from application.access_control.services.user_api_token import generate_api_token_hash
from application.core.models import Product, Product_Member
from application.core.queries.product_member import get_product_member


def create_product_api_token(product: Product, role: Roles) -> str:
    product_user_name = _get_product_user_name(product)
    user = get_user_by_username(product_user_name)
    if user:
        try:
            user.api_token  # pylint: disable=pointless-statement
            # This statement raises an exception if the user has no API token.
            raise ValidationError("Only one API token per product is allowed.")
        except API_Token.DoesNotExist:
            pass

    api_token, api_token_hash = generate_api_token_hash()

    if user:
        user.is_active = True
    else:
        user = User(username=product_user_name, is_active=True)
    user.set_unusable_password()
    user.save()

    Product_Member(product=product, user=user, role=role).save()
    API_Token(user=user, api_token_hash=api_token_hash).save()

    return api_token


def revoke_product_api_token(product: Product) -> None:
    product_user_name = _get_product_user_name(product)
    user = get_user_by_username(product_user_name)
    if not user:
        return

    try:
        api_token = user.api_token
        api_token.delete()
    except API_Token.DoesNotExist:
        pass

    product_member = get_product_member(product, user)
    if product_member:
        product_member.delete()

    user.is_active = False
    user.save()


@dataclass
class ProductAPIToken:
    id: int
    role: int


def get_product_api_tokens(product: Product) -> list[ProductAPIToken]:
    product_user_name = _get_product_user_name(product)
    user = get_user_by_username(product_user_name)
    if not user:
        return []

    product_member = get_product_member(product, user)
    if not product_member:
        return []

    return [ProductAPIToken(id=product.pk, role=product_member.role)]


def _get_product_user_name(product: Product) -> str:
    return f"-product-{product.id}-api_token-"
