import logging
import os
from importlib import import_module
from importlib.util import find_spec
from inspect import isclass
from pathlib import Path

from django.apps import AppConfig
from django.db import connection

logger = logging.getLogger("secobserve.import_observations")


class UploadObservationsConfig(AppConfig):
    name = "application.import_observations"
    verbose_name = "Upload observations"

    def ready(self):
        from application.import_observations.services.parser_registry import (  # noqa E501 pylint: disable=import-outside-toplevel
            create_manual_parser,
        )

        all_tables = connection.introspection.table_names()
        if "core_parser" in all_tables:
            # Create parser entry for manual observations
            create_manual_parser()
            # Register parsers during startup
            package_dir = str(Path(__file__).resolve().parent) + "/parsers"
            for module_name in os.listdir(package_dir):
                # Check if it is a directory
                if os.path.isdir(os.path.join(package_dir, module_name)):
                    self.register_module(module_name)

        # This forces the schema extension for DRF to be loaded
        import config.schema  # noqa F401 pylint: disable=import-outside-toplevel,unused-import

    def register_module(self, module_name):
        from application.commons.services.log_message import (  # pylint: disable=import-outside-toplevel
            format_log_message,
        )

        try:
            # Check if it is a Python module
            if find_spec(
                f"application.import_observations.parsers.{module_name}.parser"
            ):
                _register_parser(module_name)
        except Exception:
            logger.exception(  # noqa: F401 pylint: disable=import-outside-toplevel,unused-import
                format_log_message(message=f"Failed to load {module_name}")
            )


def _register_parser(module_name):
    from application.import_observations.parsers.base_parser import (  # pylint: disable=import-outside-toplevel
        BaseParser,
    )
    from application.import_observations.services.parser_registry import (  # noqa E501 pylint: disable=import-outside-toplevel
        register_parser,
    )

    # Import the module and register the classname
    module = import_module(  # nosemgrep
        f"application.import_observations.parsers.{module_name}.parser"
    )
    # nosemgrep because of rule python.lang.security.audit.non-literal-import.non-literal-import
    # This is the price you pay for a dynamic parser registry. We accept the risk.
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if (
            isclass(attribute)
            and issubclass(attribute, BaseParser)
            and attribute is not BaseParser
        ):
            register_parser(attribute)
