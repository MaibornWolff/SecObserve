from unittest.mock import patch

from application.background_tasks.periodic_tasks.core_tasks import (
    task_branch_housekeeping,
    task_expire_risk_acceptances,
)
from unittests.base_test_case import BaseTestCase


class TestCoreTasks(BaseTestCase):
    # ---------------------------------------------------------------
    # task_branch_housekeeping
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.core_tasks.delete_inactive_branches_and_set_flags")
    def test_task_branch_housekeeping(self, mock_delete_inactive_branches):
        # Execute
        task_branch_housekeeping()

        # Assert
        mock_delete_inactive_branches.assert_called_once()

    # ---------------------------------------------------------------
    # task_expire_risk_acceptances
    # ---------------------------------------------------------------

    @patch("application.background_tasks.periodic_tasks.core_tasks.expire_risk_acceptances")
    def test_task_expire_risk_acceptances(self, mock_expire_risk_acceptances):
        # Execute
        task_expire_risk_acceptances()

        # Assert
        mock_expire_risk_acceptances.assert_called_once()
