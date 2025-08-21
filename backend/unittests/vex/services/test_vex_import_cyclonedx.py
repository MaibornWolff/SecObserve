from os import path

from application.vex.models import VEX_Document, VEX_Statement
from application.vex.services.vex_import import import_vex
from application.vex.types import VEX_Document_Type
from unittests.vex.services.basetest_vex_import import BaseTestVEXImport


class TestVEXImportCycloneDX(BaseTestVEXImport):
    def test_import_integrated(self):
        self.load_vex_test()

        with open(path.dirname(__file__) + "/files/cyclonedx_vex_integrated.json") as testfile:
            import_vex(testfile)

            vex_document = VEX_Document.objects.get(
                document_id="urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
                author="SecObserve",
            )
            self.check_vex_document(vex_document, VEX_Document_Type.VEX_DOCUMENT_TYPE_CYCLONEDX)

            self.check_product()

    def test_import_dedicated(self):
        self.load_vex_test()

        with open(path.dirname(__file__) + "/files/cyclonedx_vex_test dedicated.json") as testfile:
            import_vex(testfile)

            vex_document = VEX_Document.objects.get(
                document_id="urn:uuid:fa9f9148-2935-422a-b058-20afa8cafa82",
                author="SecObserve",
            )

            vex_statements = VEX_Statement.objects.filter(document=vex_document)
            for vex_statement in vex_statements:
                print("--------------------------------------------")
                print(vars(vex_statement))
            print("--------------------------------------------")

            self.check_vex_document(vex_document, VEX_Document_Type.VEX_DOCUMENT_TYPE_CYCLONEDX)

            self.check_product()
