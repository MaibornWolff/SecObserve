from typing import Optional

from django.db.models import QuerySet

from application.core.models import Branch, Observation, Product
from application.issue_tracker.issue_trackers.base_issue_tracker import BaseIssueTracker
from application.issue_tracker.issue_trackers.github_issue_tracker import (
    GitHubIssueTracker,
)
from application.issue_tracker.issue_trackers.gitlab_issue_tracker import (
    GitLabIssueTracker,
)


def push_observations_to_issue_tracker(
    product: Product, use_branch: bool, branch: Branch = None
) -> None:
    if product.issue_tracker_active:
        if (not use_branch) or (
            use_branch and product.repository_default_branch == branch
        ):
            observations: QuerySet[Observation] = Observation.objects.filter(
                product=product, branch=product.repository_default_branch
            )
            for observation in observations:
                push_observation_to_issue_tracker(observation)


def push_observation_to_issue_tracker(observation: Observation) -> None:
    if observation.product.issue_tracker_active:
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


def push_deleted_observation_to_issue_tracker(
    product: Product, issue_id: Optional[str]
) -> None:
    if product.issue_tracker_active and issue_id:
        issue_tracker = issue_tracker_factory(product)
        issue = issue_tracker.get_issue(product, issue_id)
        if issue:
            issue_tracker.close_issue_for_deleted_observation(product, issue)


def issue_tracker_factory(product: Product) -> BaseIssueTracker:
    if product.issue_tracker_type == Product.ISSUE_TRACKER_GITHUB:
        return GitHubIssueTracker()

    if product.issue_tracker_type == Product.ISSUE_TRACKER_GITLAB:
        return GitLabIssueTracker()

    raise ValueError(f"Unknown issue tracker type: {product.issue_tracker_type}")
