import secrets
import string


def create_secret() -> str:
    alphabet = string.ascii_letters + string.digits
    secret = "".join(secrets.choice(alphabet) for i in range(32))
    return secret
