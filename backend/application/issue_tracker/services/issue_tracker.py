from typing import Optional

from huey.contrib.djhuey import db_task, task

from application.access_control.models import User
from application.commons.services.global_request import get_current_user
from application.commons.services.tasks import handle_task_exception
from application.core.models import Observation, Product
from application.issue_tracker.issue_trackers.base_issue_tracker import BaseIssueTracker
from application.issue_tracker.issue_trackers.github_issue_tracker import (
    GitHubIssueTracker,
)
from application.issue_tracker.issue_trackers.gitlab_issue_tracker import (
    GitLabIssueTracker,
)


def push_observations_to_issue_tracker(
    product: Product, observations: set[Observation]
) -> None:
    if product.issue_tracker_active:
        for observation in observations:
            push_observation_to_issue_tracker(observation, get_current_user())


@db_task()
def push_observation_to_issue_tracker(observation: Observation, user: User) -> None:
    try:
        if (
            observation.product.issue_tracker_active
            and observation.branch == observation.product.repository_default_branch
        ):
            issue_tracker = issue_tracker_factory(observation.product)

            if observation.issue_tracker_issue_id:
                issue = issue_tracker.get_issue(
                    observation.product, observation.issue_tracker_issue_id
                )
            else:
                issue = None

            # If the issue_tracker_issue_id is set but the issue does not exist, remove the id
            if observation.issue_tracker_issue_id and not issue:
                observation.issue_tracker_issue_id = ""
                observation.save()

            if observation.current_status == Observation.STATUS_OPEN:
                if issue:
                    issue_tracker.update_issue(observation, issue)
                else:
                    issue_tracker.create_issue(observation)
            else:
                if issue:
                    issue_tracker.close_issue(observation, issue)
    except Exception as e:
        handle_task_exception(e, user)


@task()
def push_deleted_observation_to_issue_tracker(
    product: Product, issue_id: Optional[str], user: User
) -> None:
    try:
        if product.issue_tracker_active and issue_id:
            issue_tracker = issue_tracker_factory(product)
            issue = issue_tracker.get_issue(product, issue_id)
            if issue:
                issue_tracker.close_issue_for_deleted_observation(product, issue)
    except Exception as e:
        handle_task_exception(e, user)


def issue_tracker_factory(product: Product) -> BaseIssueTracker:
    if product.issue_tracker_type == Product.ISSUE_TRACKER_GITHUB:
        return GitHubIssueTracker()

    if product.issue_tracker_type == Product.ISSUE_TRACKER_GITLAB:
        return GitLabIssueTracker()

    raise ValueError(f"Unknown issue tracker type: {product.issue_tracker_type}")
