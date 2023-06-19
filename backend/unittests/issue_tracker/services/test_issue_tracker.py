from unittest.mock import call, patch

from django.core.management import call_command

from application.core.models import Observation, Product
from application.issue_tracker.issue_trackers.base_issue_tracker import Issue
from application.issue_tracker.issue_trackers.github_issue_tracker import (
    GitHubIssueTracker,
)
from application.issue_tracker.issue_trackers.gitlab_issue_tracker import (
    GitLabIssueTracker,
)
from application.issue_tracker.services.issue_tracker import (
    issue_tracker_factory,
    push_deleted_observation_to_issue_tracker,
    push_observation_to_issue_tracker,
    push_observations_to_issue_tracker,
)
from unittests.base_test_case import BaseTestCase


class TestIssueTracker(BaseTestCase):
    def setUp(self):
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")

    @patch(
        "application.issue_tracker.services.issue_tracker.push_observation_to_issue_tracker"
    )
    def test_push_observations_to_issue_tracker_not_active(self, mock):
        product = Product.objects.get(pk=1)
        push_observations_to_issue_tracker(product, False)
        mock.assert_not_called()

    @patch(
        "application.issue_tracker.services.issue_tracker.push_observation_to_issue_tracker"
    )
    def test_push_observations_to_issue_tracker(self, mock):
        product = Product.objects.get(pk=1)
        product.issue_tracker_active = True
        observation = Observation.objects.get(pk=1)

        push_observations_to_issue_tracker(
            product, True, observation.product.repository_default_branch
        )

        mock.assert_called_once_with(observation)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_observation_to_issue_tracker_not_active(self, mock):
        observation = Observation.objects.get(pk=1)
        push_observation_to_issue_tracker(observation)
        mock.assert_not_called()

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_observation_to_issue_tracker_open_no_id_no_issue(self, mock):
        mock.return_value.get_issue.return_value = None

        observation = Observation.objects.get(pk=1)
        observation.product.issue_tracker_active = True
        observation.current_status = Observation.STATUS_OPEN

        push_observation_to_issue_tracker(observation)

        expected_calls = [call(observation.product), call().create_issue(observation)]
        mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    @patch("application.core.models.Observation.save")
    def test_push_observation_to_issue_tracker_open_with_id_no_issue(
        self, observation_mock, factory_mock
    ):
        factory_mock.return_value.get_issue.return_value = None

        observation = Observation.objects.get(pk=1)
        observation.product.issue_tracker_active = True
        observation.current_status = Observation.STATUS_OPEN
        observation.issue_tracker_issue_id = "123"

        push_observation_to_issue_tracker(observation)

        expected_calls = [
            call(observation.product),
            call().get_issue(observation.product, "123"),
            call().create_issue(observation),
        ]
        observation_mock.assert_called_once()
        factory_mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    @patch("application.core.models.Observation.save")
    def test_push_observation_to_issue_tracker_open_with_id_with_issue(
        self, observation_mock, factory_mock
    ):
        issue = Issue(id=1, title="title", description="description", labels="labels")
        factory_mock.return_value.get_issue.return_value = issue

        observation = Observation.objects.get(pk=1)
        observation.product.issue_tracker_active = True
        observation.current_status = Observation.STATUS_OPEN
        observation.issue_tracker_issue_id = "123"

        push_observation_to_issue_tracker(observation)

        expected_calls = [
            call(observation.product),
            call().get_issue(observation.product, "123"),
            call().update_issue(observation, issue),
        ]
        observation_mock.assert_not_called()
        factory_mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    @patch("application.core.models.Observation.save")
    def test_push_observation_to_issue_tracker_closed_no_id_no_issue(
        self, observation_mock, factory_mock
    ):
        factory_mock.return_value.get_issue.return_value = None

        observation = Observation.objects.get(pk=1)
        observation.product.issue_tracker_active = True
        observation.current_status = Observation.STATUS_NOT_AFFECTED

        push_observation_to_issue_tracker(observation)

        expected_calls = [call(observation.product)]
        observation_mock.assert_not_called()
        factory_mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    @patch("application.core.models.Observation.save")
    def test_push_observation_to_issue_tracker_closed_with_id_with_issue(
        self, observation_mock, factory_mock
    ):
        issue = Issue(id=1, title="title", description="description", labels="labels")
        factory_mock.return_value.get_issue.return_value = issue

        observation = Observation.objects.get(pk=1)
        observation.product.issue_tracker_active = True
        observation.current_status = Observation.STATUS_FALSE_POSITIVE
        observation.issue_tracker_issue_id = "123"

        push_observation_to_issue_tracker(observation)

        expected_calls = [
            call(observation.product),
            call().get_issue(observation.product, "123"),
            call().close_issue(observation, issue),
        ]
        observation_mock.assert_not_called()
        factory_mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_deleted_observation_not_active_no_id(self, mock):
        product = Product.objects.get(pk=1)
        push_deleted_observation_to_issue_tracker(product, "")
        mock.assert_not_called()

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_deleted_observation_active_no_id(self, mock):
        product = Product.objects.get(pk=1)
        product.issue_tracker_active = True
        push_deleted_observation_to_issue_tracker(product, "")
        mock.assert_not_called()

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_deleted_observation_not_active_with_id(self, mock):
        product = Product.objects.get(pk=1)
        push_deleted_observation_to_issue_tracker(product, "123")
        mock.assert_not_called()

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_deleted_observation_active_with_id_no_issue(self, mock):
        mock.return_value.get_issue.return_value = None
        product = Product.objects.get(pk=1)
        product.issue_tracker_active = True
        push_deleted_observation_to_issue_tracker(product, "123")
        expected_calls = [call(product), call().get_issue(product, "123")]
        mock.assert_has_calls(expected_calls, any_order=False)

    @patch("application.issue_tracker.services.issue_tracker.issue_tracker_factory")
    def test_push_deleted_observation_active_with_id_with_issue(self, mock):
        issue = Issue(id=1, title="title", description="description", labels="labels")
        mock.return_value.get_issue.return_value = issue
        product = Product.objects.get(pk=1)
        product.issue_tracker_active = True
        push_deleted_observation_to_issue_tracker(product, "123")
        expected_calls = [
            call(product),
            call().get_issue(product, "123"),
            call().close_issue_for_deleted_observation(product, issue),
        ]
        mock.assert_has_calls(expected_calls, any_order=False)

    def test_issue_tracker_factory_GitHub(self):
        product = Product.objects.get(pk=1)
        product.issue_tracker_type = Product.ISSUE_TRACKER_GITHUB
        self.assertIsInstance(issue_tracker_factory(product), GitHubIssueTracker)

    def test_issue_tracker_factory_GitLab(self):
        product = Product.objects.get(pk=1)
        product.issue_tracker_type = Product.ISSUE_TRACKER_GITLAB
        self.assertIsInstance(issue_tracker_factory(product), GitLabIssueTracker)

    def test_issue_tracker_exception(self):
        product = Product.objects.get(pk=1)
        product.issue_tracker_type = "invalid"
        with self.assertRaises(ValueError):
            issue_tracker_factory(product)
