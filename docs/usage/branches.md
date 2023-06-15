# Working with branches

## Branches in the product

A product has a list of branches. They can either be created manually from the **Branches** tab of the product or will be created automatically, when observations are imported via the the API or the GitHub actions / GitLab templates when a branch name is used that didn't exist before for that product.

![Branches in the product](../assets/images/screenshot_product_branches.png)

The list of branches shows the severities of open observations for each branch.

## Repository default branch

The **Repository default branch** should always be set, when branches are used in the observations. The metrics on the dashboard and on the **Metrics** tab as well as the severites in the header when showing a product are calculated using the observations where the default branch is set.

The repository default branch can be set manually while editing a product. If it is not set manually, it will be set automatically after importing observations with the branch name used for the import.

![Branches in the product](../assets/images/screenshot_product_default_branch.png)
