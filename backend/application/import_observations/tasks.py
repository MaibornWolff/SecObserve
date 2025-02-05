import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.commons import settings_static
from application.commons.models import Settings
from application.commons.services.tasks import handle_task_exception
from application.import_observations.models import Api_Configuration, Product
from application.import_observations.services.import_observations import (
    ApiImportParameters,
    api_import_observations,
)
from application.import_observations.services.osv_scanner import scan_product

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
                api_import_parameters = ApiImportParameters(
                    api_configuration=api_configuration,
                    branch=api_configuration.automatic_import_branch,
                    service=api_configuration.automatic_import_service,
                    docker_image_name_tag=api_configuration.automatic_import_docker_image_name_tag,
                    endpoint_url=api_configuration.automatic_import_endpoint_url,
                    kubernetes_cluster=api_configuration.automatic_import_kubernetes_cluster,
                )
                (
                    observations_new,
                    observations_updated,
                    observations_resolved,
                ) = api_import_observations(api_import_parameters)
                logger.info(
                    "API import - %s: %s new, %s updated, %s resolved",
                    api_configuration,
                    observations_new,
                    observations_updated,
                    observations_resolved,
                )
            except Exception as e:
                logger.warning(
                    "API import - %s: failed with exception", api_configuration
                )
                handle_task_exception(e, product=api_configuration.product)

    except Exception as e:
        handle_task_exception(e)

    logger.info("--- API import - finished ---")

    logger.info("--- OSV scanning - start ---")

    try:
        settings = Settings.load()
        if not settings.feature_automatic_osv_scanning:
            logger.info("OSV scanning is disabled in settings")
            return

        products = Product.objects.filter(
            osv_enabled=True, automatic_osv_scanning_enabled=True
        )
        for product in products:
            try:
                (
                    observations_new,
                    observations_updated,
                    observations_resolved,
                ) = scan_product(product)
                logger.info(
                    "OSV scanning - %s: %s new, %s updated, %s resolved",
                    product,
                    observations_new,
                    observations_updated,
                    observations_resolved,
                )
            except Exception as e:
                logger.warning("OSV scanning - %s: failed with exception", product)
                handle_task_exception(e, product=product)

    except Exception as e:
        handle_task_exception(e)

    logger.info("--- OSV scanning - finished ---")
