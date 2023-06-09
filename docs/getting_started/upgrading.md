# Upgrading

## Generic upgrade procedure

* Frontend and backend shall always be started with the same version number. 

* The Docker Compose `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml` in the GitHub repository always use the most recent released version of SecObserve.

* The database structure will automatically be updated to the reflect the latest changes, when the backend container gets started. **Always make a backup of your database before upgrading, in case something should go wrong.**

* There will be specific upgrade instructions if necessary, e.g. when there are new configuration parameters.

## Release 0.9.1

**Breaking changes**

* The SSLyze parser has been replaced by the CryptoLyzer parser due to licensing reasons. Even though the SSLyze parser may still be seen in the list of parsers, you cannot use it for imports anymore. The CryptoLyter parser generates the same kind of results, adding information about signature algorithms.

* The project name `secobserve_prod` has been set in `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml`. This was necessary to assign defined network names, but it changes the name of the database volume. You need to dump the database content to a file before the upgrade and restore it after the upgrade.
