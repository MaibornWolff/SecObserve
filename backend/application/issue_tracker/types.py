class Issue_Tracker:
    ISSUE_TRACKER_GITHUB = "GitHub"
    ISSUE_TRACKER_GITLAB = "GitLab"
    ISSUE_TRACKER_JIRA = "Jira"

    ISSUE_TRACKER_TYPE_CHOICES = [
        (ISSUE_TRACKER_GITHUB, ISSUE_TRACKER_GITHUB),
        (ISSUE_TRACKER_GITLAB, ISSUE_TRACKER_GITLAB),
        (ISSUE_TRACKER_JIRA, ISSUE_TRACKER_JIRA),
    ]
