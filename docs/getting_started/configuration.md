# Configuration

## Deployment

A part of the configuation is done with environment variables, which need to be set when deploying SecObserve. How this is done depends on the deployment method, see [Installation](installation.md).

#### Backend

| Environment variable   | Optionality | Description |
|------------------------|:-----------:|-------------|
| `AAD_CLIENT_ID`        | optional    | Only for authentication with Azure AD: Client ID from the Azure app registration. |
| `AAD_TENANT_ID`        | optional    | Only for authentication with Azure AD: Tenant ID of the Azure subscription. |
| `ADMIN_USER`           | mandatory   | Username of the administration user. The user will be created at the fist start of the backend. |
| `ADMIN_EMAIL`          | optional    | E-Mail of the administration user. |
| `ADMIN_PASSWORD`       | optional    | Initial password of the admin user. If it is not set, a random password will be created during startup and shown in the log. |
| `ALLOWED_HOSTS`        | mandatory   | Hostname of the backend, see [Django settings ALLOWED_HOSTS](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts) |
| `CORS_ALLOWED_ORIGINS` | mandatory   | URL of the frontend that is authorized to make cross-site HTTP requests. |
| `DATABASE_HOST`        | mandatory   | Which host to use when connecting to the database. |
| `DATABASE_DB`          | mandatory   | The name of the database to use. |
| `DATABASE_PORT`        | mandatory   | The port to use when connecting to the database. |
| `DATABASE_USER`        | mandatory   | The username to use when connecting to the database. |
| `DATABASE_PASSWORD`    | mandatory   | The password to use when connecting to the database. |
| `DATABASE_ENGINE`      | mandatory   | The database backend to use. Supported database backends are `django.db.backends.mysql` and `django.db.backends.postgresql` |
| `MYSQL_AZURE`          | optional    | Must be set if Azure Database for MySQL is used, to use the necessary SSL certificate. For **MySQL Flexible Server** it needs to have the value `flexible`, for **MySQL Single Server** the the value needs to be `single`. See [Connect using mysql command-line client with TLS/SSL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-connect-tls-ssl#connect-using-mysql-command-line-client-with-tlsssl) and [Configure SSL connectivity in your application to securely connect to Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/single-server/how-to-configure-ssl#step-1-obtain-ssl-certificate).
| `DJANGO_SECRET_KEY`    | mandatory   | A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value with at least 50 characters, see [Django settings SECRET_KEY](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).
| `FIELD_ENCRYPTION_KEY` | mandatory   | Key to encrypt fields like the JWT secret. See [Generating an Encryption Key](https://gitlab.com/lansharkconsulting/django/django-encrypted-model-fields#generating-an-encryption-key) how to generate the key. |


#### Frontend

| Environment variable           | Optionality | Description |
|--------------------------------|:-----------:|-------------|
| `AAD_ENABLE`                   | mandatory   | `true`: Azure AD authentication is active, `false`: otherwise. |
| `AAD_AUTHORITY`                | mandatory   | The authority is a URL that indicates a directory that MSAL can request tokens from, typically `https://login.microsoftonline.com/<TENANT>/` |
| `AAD_CLIENT_ID`                | mandatory   | The client ID is the unique *Application (client) ID* assigned to your app by Azure AD when the app was registered. |
| `AAD_REDIRECT_URI`             | mandatory   | The redirect URI is the URI the identity provider will send the security tokens back to. To be set with the URL of the frontend. |
| `AAD_POST_LOGOUT_REDIRECT_URI` | mandatory   | The post logout redirect URI is the URI that will be called after logout. To be set with the URL of the frontend. |
| `AAD_SCOPE`                    | mandatory   | The scope is a permission that have been granted to the client applications, see [Scopes and permissions in the Microsoft identity platform](https://learn.microsoft.com/en-us/azure/active-directory/develop/scopes-oidc). Might be something like `<AAD_CLIENT_ID>/.default` |
| `API_BASE_URL`                 | mandatory   | URL where to find the backend API, e.g. `https:\\secobserve-backend.example.com/api`. |

All the `AAD_*` environment variables are needed for technical reasons. If `AAD_ENABLE` is set to `false`, the other `AAD_*` environment variables can be set to `dummy` or something similar.

## Admin user interface

SecObserve provides an administration user interface to manage users and some system-wide configurations. It can be accessed via `<BACKEND_URL>/admin` by users where the flag `Superuser status` is set. 

The entries in section *CONSTANCE / Config* should be checked and adjusted if necessary after installing SecObserve.
