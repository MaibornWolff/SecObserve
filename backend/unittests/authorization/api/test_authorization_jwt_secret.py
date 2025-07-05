from application.access_control.models import JWT_Secret
from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationJWTSecret(TestAuthorizationBase):
    def test_authorization_jwt_secret(self):

        secret_old = JWT_Secret.load().secret
        self._test_api(APITest("db_admin", "post", "/api/jwt_secret/reset/", None, 204, None))
        secret_new = JWT_Secret.load().secret
        self.assertNotEqual(secret_old, secret_new)
        self.assertEqual(32, len(secret_new))

        self._test_api(APITest("db_internal_write", "post", "/api/jwt_secret/reset/", None, 403, None))
