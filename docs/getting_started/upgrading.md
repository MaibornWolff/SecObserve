# Upgrading

## Generic upgrade procedure

* Frontend and backend shall always be started with the same version number. 

* The Docker Compose `docker-compose-prod-mysql.yml` and `docker-compose-prod-postgres.yml` in the GitHub repository always use the most recent released version of SecObserve.

* The database structure will automatically be updated to the reflect the latest changes, when the backend container gets started. **Always make a backup of your database before upgrading, in case something should go wrong.**

* There will be specific upgrade instructions if necessary, e.g. when there are new configuration parameters.
