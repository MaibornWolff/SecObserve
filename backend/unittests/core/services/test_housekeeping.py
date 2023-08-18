from datetime import timedelta
from unittest.mock import Mock, call, patch

from constance.test import override_config
from django.core.management import call_command
from django.utils import timezone

from application.core.models import Branch, Product
from application.core.services.housekeeping import (
    delete_inactive_branches,
    delete_inactive_branches_for_product,
)
from unittests.base_test_case import BaseTestCase


class TestHousekeeping(BaseTestCase):
    def setUp(self) -> None:
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")
        branch = Branch.objects.get(name="db_branch_internal_dev")
        branch.last_import = timezone.now() - timedelta(days=10)
        branch.save()
        branch = Branch.objects.get(name="db_branch_internal_main")
        branch.last_import = timezone.now() - timedelta(days=10)
        branch.save()

        product = Product.objects.get(name="db_product_internal")
        product.product_group = None
        product.save()

        return super().setUp()

    @patch(
        "application.core.services.housekeeping.delete_inactive_branches_for_product"
    )
    def test_delete_inactive_branches(
        self, mock_delete_inactive_branches_for_product: Mock
    ):
        delete_inactive_branches()

        expected_calls = [
            call(Product.objects.get(name="db_product_internal")),
            call(Product.objects.get(name="db_product_external")),
        ]
        mock_delete_inactive_branches_for_product.assert_has_calls(expected_calls)
        self.assertEqual(mock_delete_inactive_branches_for_product.call_count, 2)

    @override_config(BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS=9)
    def test_delete_inactive_branches_for_product_delete(self):
        product = Product.objects.get(name="db_product_internal")
        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_dev")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

        try:
            Branch.objects.get(name="db_branch_internal_main")
            self.fail("Branch should have been deleted")
        except Branch.DoesNotExist:
            pass

    @override_config(BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS=9)
    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_not_active(self):
        product = Product.objects.get(name="db_product_internal")
        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS=11)
    def test_delete_inactive_branches_for_product_too_early(self):
        product = Product.objects.get(name="db_product_internal")
        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS=9)
    @override_config(BRANCH_HOUSEKEEPING_EXEMPT_BRANCHES="db_branch_internal_m.*")
    def test_delete_inactive_branches_for_product_exempt(self):
        product = Product.objects.get(name="db_product_internal")

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_KEEP_INACTIVE_DAYS=9)
    def test_delete_inactive_branches_for_product_product_not_active(self):
        product = Product.objects.get(name="db_product_internal")
        product.repository_branch_housekeeping_active = False
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_specific_delete(self):
        product_group = Product.objects.get(name="db_product_group")
        product_group.repository_branch_housekeeping_active = None
        product_group.repository_branch_housekeeping_keep_inactive_days = 11
        product_group.save()
        product = Product.objects.get(name="db_product_internal")
        product.product_group = product_group
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 9
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            self.fail("Branch should have been deleted")
        except Branch.DoesNotExist:
            pass

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_specific_too_early(self):
        product = Product.objects.get(name="db_product_internal")
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 11
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_specific_exempt(self):
        product = Product.objects.get(name="db_product_internal")
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 9
        product.repository_branch_housekeeping_exempt_branches = (
            "db_branch_internal_m.*"
        )
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_specific_protected(self):
        product = Product.objects.get(name="db_product_internal")
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 9
        product.save()
        branch = Branch.objects.get(name="db_branch_internal_main")
        branch.housekeeping_protect = True
        branch.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")


    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_group_not_active(self):
        product_group = Product.objects.get(name="db_product_group")
        product_group.repository_branch_housekeeping_active = False
        product_group.save()
        product = Product.objects.get(name="db_product_internal")
        product.product_group = product_group
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 9
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_group_too_early(self):
        product_group = Product.objects.get(name="db_product_group")
        product_group.repository_branch_housekeeping_active = True
        product_group.repository_branch_housekeeping_keep_inactive_days = 11
        product_group.save()
        product = Product.objects.get(name="db_product_internal")
        product.product_group = product_group
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 11
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")

    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_group_exempt(self):
        product_group = Product.objects.get(name="db_product_group")
        product_group.repository_branch_housekeeping_active = True
        product_group.repository_branch_housekeeping_keep_inactive_days = 9
        product_group.repository_branch_housekeeping_exempt_branches = (
            "db_branch_internal_m.*"
        )
        product_group.save()
        product = Product.objects.get(name="db_product_internal")
        product.product_group = product_group
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 9
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            pass
        except Branch.DoesNotExist:
            self.fail("Branch should not have been deleted")


    @override_config(BRANCH_HOUSEKEEPING_ACTIVE=False)
    def test_delete_inactive_branches_for_product_product_group_delete(self):
        product_group = Product.objects.get(name="db_product_group")
        product_group.repository_branch_housekeeping_active = True
        product_group.repository_branch_housekeeping_keep_inactive_days = 9
        product_group.save()
        product = Product.objects.get(name="db_product_internal")
        product.product_group = product_group
        product.repository_branch_housekeeping_active = True
        product.repository_branch_housekeeping_keep_inactive_days = 11
        product.save()

        delete_inactive_branches_for_product(product)

        try:
            Branch.objects.get(name="db_branch_internal_main")
            self.fail("Branch should have been deleted")
        except Branch.DoesNotExist:
            pass
