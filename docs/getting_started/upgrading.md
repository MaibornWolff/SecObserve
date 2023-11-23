# Upgrading

## Generic upgrade procedure

* Frontend and backend shall always be started with the same version number. 

* The Docker Compose `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml` in the GitHub repository always use the most recent released version of SecObserve.

* The database structure will automatically be updated to the reflect the latest changes, when the backend container gets started. **Always make a backup of your database before upgrading, in case something should go wrong.**

* There will be specific upgrade instructions if necessary, e.g. when there are new configuration parameters.

## Release 1.1.0

**Breaking changes**

* When OIDC authentication is used, the environment variable `OIDC_CLIENT_ID` needs to be set for the backend as well. See [Configuration](configuration.md) and [OpenID Connect authentication](../integrations/oidc_authentication.md) for details.

## Release 1.0.0

**Breaking changes**

* SecObserve now supports different OpenID Connect providers for authentication and the Microsoft specific dependencies have been removed. Thus the `AAD_` configuration parameters are not valid anymore and have been replaced with `OIDC_` parameters, see [Configuration](configuration.md) and [OpenID Connect authentication](../integrations/oidc_authentication.md) for details.

## Release 0.9.9

**Breaking changes**

* The value of the configuration parameter `MYSQL_AZURE` has been changed from `true` to `flexible` or `single`, depending on the type of Azure Database for MySQL. See [Configuration](configuration.md) for details.

## Release 0.9.1

**Breaking changes**

* The SSLyze parser has been replaced by the CryptoLyzer parser due to licensing reasons. Even though the SSLyze parser may still be seen in the list of parsers, you cannot use it for imports anymore. The CryptoLyter parser generates the same kind of results, adding information about signature algorithms.

* The project name `secobserve_prod` has been set in `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml`. This was necessary to assign defined network names, but it changes the name of the database volume. You need to dump the database content to a file before the upgrade and restore it after the upgrade.
