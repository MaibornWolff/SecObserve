from application.core.models import Product
from application.core.queries.product import get_branches_by_product


def set_repository_default_branch(product: Product) -> None:
    if not product.repository_default_branch:
        current_repository_default_branch = product.repository_default_branch
        new_repository_default_branch = product.repository_default_branch
        branches = get_branches_by_product(product)
        if not branches:
            new_repository_default_branch = None
        else:
            if len(branches) == 1:
                new_repository_default_branch = branches[0]
            else:
                for branch in branches:
                    if branch.name == "main":
                        new_repository_default_branch = branch
                        break

        if new_repository_default_branch != current_repository_default_branch:
            product.repository_default_branch = new_repository_default_branch
            product.save()
