import string
import secrets

from application.access_control.models import JWT_Secret


def get_secret() -> str:
    jwt_secrets = JWT_Secret.objects.all()
    if len(jwt_secrets) == 1:
        return jwt_secrets[0].secret
    else:
        for jwt_secret in jwt_secrets:
            jwt_secret.delete()
        new_secret = _create_secret()
        JWT_Secret(secret=new_secret).save()
        return new_secret


def _create_secret() -> str:
    alphabet = string.ascii_letters + string.digits
    secret = "".join(secrets.choice(alphabet) for i in range(32))
    return secret
