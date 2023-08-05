import os
import resource

from django.apps import AppConfig
from huey.contrib.djhuey import HUEY as huey


class UtilsConfig(AppConfig):
    name = "application.commons"
    verbose_name = "Commons"

    def ready(self):
        try:
            import application.commons.signals  # noqa F401 pylint: disable=import-outside-toplevel, unused-import
        except ImportError:
            pass

        if os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
            with open(
                "/sys/fs/cgroup/memory/memory.limit_in_bytes", encoding="utf-8"
            ) as limit:
                mem = int(limit.read())
                resource.setrlimit(resource.RLIMIT_AS, (mem, mem))

        huey.flush_locks(
            "import_epss", "calculate_product_metrics", "branch_housekeeping"
        )

        # This forces the schema extension for DRF to be loaded
        import config.schema  # noqa: F401 pylint: disable=import-outside-toplevel, unused-import
