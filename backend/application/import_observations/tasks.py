import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.models import Settings
from application.commons.services.tasks import handle_task_exception
from application.import_observations.models import Api_Configuration
from application.import_observations.services.import_observations import (
    api_import_observations,
)

logger = logging.getLogger("secobserve.import_observations")


@db_periodic_task(
    crontab(
        minute=settings_static.api_import_crontab_minute,
        hour=settings_static.api_import_crontab_hour,
    )
)
@lock_task("api_import")
def task_api_import() -> None:
    logger.info("--- API import - start ---")

    try:
        settings = Settings.load()
        if not settings.feature_automatic_api_import:
            logger.info("API import is disabled in settings")
            return

        api_configurations = Api_Configuration.objects.filter(
            automatic_import_enabled=True
        )
        for api_configuration in api_configurations:
            try:
                (
                    observations_new,
                    observations_updated,
                    observations_resolved,
                ) = api_import_observations(
                    api_configuration,
                    api_configuration.automatic_import_branch,
                    api_configuration.automatic_import_service,
                    api_configuration.automatic_import_docker_image_name_tag,
                    api_configuration.automatic_import_endpoint_url,
                    api_configuration.automatic_import_kubernetes_cluster,
                )
                logger.info(
                    f"API import - {api_configuration}: "
                    + f"{observations_new} new, {observations_updated} updated, {observations_resolved} resolved"
                )
            except Exception as e:
                logger.warning(
                    "API import - %s: failed with exception", api_configuration
                )
                handle_task_exception(e)

    except Exception as e:
        handle_task_exception(e)

    logger.info("--- API import - finished ---")
