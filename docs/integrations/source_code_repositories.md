# Source code repositories

Observations can have a source file plus start and end lines as an origin. During the assessment of the observation it is often helpful to view the source code.

## Setting the repository in a product

When creating or editing a product, the field `Repository prefix` can be set. This needs to be the prefix of the URL to show a file in the repository, including the branch. For GitLab it is something like `https://gitlab.maibornwolff.de/secobserve/secobserve/-/blob/dev`, for GitHub it looks like `https://github.com/MaibornWolff/codecharta/blob/main`.

## Showing the link 

If the `Repository prefix` is set in the product and the observation has a source file as an origin, then name of the source file will be shown as a link to the source in the repository.