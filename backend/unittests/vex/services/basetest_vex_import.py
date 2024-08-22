from os import path
from unittest import TestCase

from application.core.models import Observation, Product
from application.core.types import Status
from application.import_observations.models import Parser
from application.import_observations.services.import_observations import (
    FileUploadParameters,
    file_upload_observations,
)
from application.vex.models import VEX_Document, VEX_Statement
from application.vex.types import VEX_Document_Type, VEX_Justification, VEX_Status


class BaseTestVEXImport(TestCase):
    def load_vex_test(self, short: bool = False) -> None:
        purl_vex_test = (
            "pkg:github/MaibornWolff/VEX_Test"
            if short
            else "pkg:github/MaibornWolff/VEX_Test@v1.7.0"
        )
        product = Product.objects.create(
            purl=purl_vex_test,
            name="VEX_Test",
            description="VEX Test Product",
        )
        filename = (
            "/files/trivy_poetry_short.json" if short else "/files/trivy_poetry.json"
        )
        with open(path.dirname(__file__) + filename) as testfile:
            file_upload_parameter = FileUploadParameters(
                product=product,
                branch=None,
                parser=Parser.objects.get(name="CycloneDX"),
                file=testfile,
                service="",
                docker_image_name_tag="",
                endpoint_url="",
                kubernetes_cluster="",
            )
            file_upload_observations(file_upload_parameter)

    def tearDown(self):
        VEX_Statement.objects.all().delete()
        VEX_Document.objects.all().delete()
        Observation.objects.filter(product__name="VEX_Test").delete()
        Product.objects.filter(name="VEX_Test").delete()

    def check_vex_document(
        self, vex_document: VEX_Document, document_type: str, short: bool = False
    ) -> None:
        self.assertEqual(document_type, vex_document.type)
        self.assertEqual("1", vex_document.version)
        self.assertEqual("vendor", vex_document.role)
        if document_type == VEX_Document_Type.VEX_DOCUMENT_TYPE_CSAF:
            self.assertEqual(
                "2024-07-14T11:12:19.671904+00:00",
                vex_document.initial_release_date.isoformat(),
            )
            self.assertEqual(
                "2024-07-14T11:12:19.671919+00:00",
                vex_document.current_release_date.isoformat(),
            )
        else:
            self.assertEqual(
                "2024-07-14T11:17:57.668593+00:00",
                vex_document.initial_release_date.isoformat(),
            )
            self.assertEqual(
                "2024-07-14T11:17:57.668609+00:00",
                vex_document.current_release_date.isoformat(),
            )

        vex_statements = VEX_Statement.objects.filter(document=vex_document)
        self.assertEqual(13, len(vex_statements))

        found_49083 = False
        found_0727 = False
        found_4340 = False

        purl_vex_test = (
            "pkg:github/MaibornWolff/VEX_Test"
            if short
            else "pkg:github/MaibornWolff/VEX_Test@v1.7.0"
        )
        purl_cryptography = (
            "pkg:pypi/cryptography" if short else "pkg:pypi/cryptography@41.0.5"
        )
        purl_sqlparse = "pkg:pypi/sqlparse" if short else "pkg:pypi/sqlparse@0.4.4"

        for vex_statement in vex_statements:
            if (
                vex_statement.vulnerability_id == "CVE-2023-49083"
                and vex_statement.component_purl == purl_cryptography
            ):
                found_49083 = True
                self.assertTrue(
                    vex_statement.description.startswith(
                        "cryptography is a package designed to expose cryptographic primitives and recipes to Python developers."
                    )
                )
                self.assertEqual(
                    VEX_Status.VEX_STATUS_NOT_AFFECTED, vex_statement.status
                )
                self.assertEqual(
                    VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,
                    vex_statement.justification,
                )
                if document_type == VEX_Document_Type.VEX_DOCUMENT_TYPE_CSAF:
                    self.assertEqual("", vex_statement.impact)
                else:
                    self.assertEqual(
                        "Not affected for VEX test case", vex_statement.impact
                    )

                self.assertEqual("", vex_statement.remediation)
                self.assertEqual(
                    purl_vex_test,
                    vex_statement.product_purl,
                )

            if (
                vex_statement.vulnerability_id == "CVE-2024-0727"
                and vex_statement.component_purl == purl_cryptography
            ):
                found_0727 = True
                self.assertTrue(
                    vex_statement.description.startswith(
                        "Issue summary: Processing a maliciously formatted PKCS12 file"
                    )
                )
                self.assertEqual(VEX_Status.VEX_STATUS_AFFECTED, vex_statement.status)
                self.assertEqual(
                    "",
                    vex_statement.justification,
                )
                self.assertEqual("", vex_statement.impact)
                self.assertEqual(
                    "Upgrade cryptography to version 42.0.2", vex_statement.remediation
                )
                self.assertEqual(
                    purl_vex_test,
                    vex_statement.product_purl,
                )

            if (
                vex_statement.vulnerability_id == "CVE-2024-4340"
                and vex_statement.component_purl == purl_sqlparse
            ):
                found_4340 = True
                self.assertTrue(
                    vex_statement.description.startswith(
                        "Passing a heavily nested list to sqlparse.parse()"
                    )
                )
                self.assertEqual(
                    VEX_Status.VEX_STATUS_UNDER_INVESTIGATION, vex_statement.status
                )
                self.assertEqual(
                    "",
                    vex_statement.justification,
                )
                self.assertEqual("", vex_statement.impact)
                self.assertEqual("", vex_statement.remediation)
                self.assertEqual(
                    purl_vex_test,
                    vex_statement.product_purl,
                )

        self.assertTrue(found_49083)
        self.assertTrue(found_0727)
        self.assertTrue(found_4340)

    def check_product(self, short: bool = False) -> None:
        purl_vex_test = (
            "pkg:github/MaibornWolff/VEX_Test"
            if short
            else "pkg:github/MaibornWolff/VEX_Test@v1.7.0"
        )
        purl_cryptography = (
            "pkg:pypi/cryptography" if short else "pkg:pypi/cryptography@41.0.5"
        )
        purl_sqlparse = "pkg:pypi/sqlparse" if short else "pkg:pypi/sqlparse@0.4.4"

        product = Product.objects.get(purl=purl_vex_test)
        observations = Observation.objects.filter(
            product=product, current_status=Status.STATUS_OPEN
        )
        self.assertEqual(11, len(observations))

        observation = Observation.objects.get(
            product=product,
            vulnerability_id="CVE-2023-49083",
            origin_component_purl=purl_cryptography,
        )
        self.assertEqual(Status.STATUS_NOT_AFFECTED, observation.current_status)
        self.assertEqual(Status.STATUS_NOT_AFFECTED, observation.vex_status)
        self.assertEqual(
            VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,
            observation.current_vex_justification,
        )
        self.assertEqual(
            VEX_Justification.STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,
            observation.vex_vex_justification,
        )

        observation = Observation.objects.get(
            product=product,
            vulnerability_id="CVE-2024-4340",
            origin_component_purl=purl_sqlparse,
        )
        self.assertEqual(Status.STATUS_IN_REVIEW, observation.current_status)
        self.assertEqual(Status.STATUS_IN_REVIEW, observation.vex_status)
        self.assertEqual("", observation.current_vex_justification)
        self.assertEqual("", observation.vex_vex_justification)
