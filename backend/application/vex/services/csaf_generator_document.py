from application.__init__ import __version__
from application.vex.models import CSAF, CSAF_Revision
from application.vex.types import (
    CSAFTLP,
    CSAFDistribution,
    CSAFDocument,
    CSAFEngine,
    CSAFGenerator,
    CSAFPublisher,
    CSAFRevisionHistory,
    CSAFRoot,
    CSAFTracking,
)


def create_csaf_root(csaf: CSAF) -> CSAFRoot:
    csaf_publisher = CSAFPublisher(
        name=csaf.publisher_name,
        category=csaf.publisher_category,
        namespace=csaf.publisher_namespace,
    )

    csaf_engine = CSAFEngine(
        name="SecObserve",
        version=__version__,
    )

    csaf_generator = CSAFGenerator(
        engine=csaf_engine,
    )

    csaf_revision_history_list = []
    csaf_revisions = CSAF_Revision.objects.filter(csaf=csaf)
    for csaf_revision in csaf_revisions:
        csaf_revision_history = CSAFRevisionHistory(
            date=csaf_revision.date.isoformat(),
            number=str(csaf_revision.version),
            summary=csaf_revision.summary,
        )
        csaf_revision_history_list.append(csaf_revision_history)

    tracking_id = _get_document_id(csaf.document_id_prefix, csaf.document_base_id, csaf.version)

    csaf_tracking = CSAFTracking(
        id=tracking_id,
        initial_release_date=csaf.tracking_initial_release_date.isoformat(),
        current_release_date=csaf.tracking_current_release_date.isoformat(),
        version=str(csaf.version),
        status=csaf.tracking_status,
        generator=csaf_generator,
        revision_history=csaf_revision_history_list,
    )

    csaf_tlp = CSAFTLP(label=csaf.tlp_label)
    csaf_distribution = CSAFDistribution(tlp=csaf_tlp)

    csaf_document = CSAFDocument(
        category="csaf_vex",
        csaf_version="2.0",
        title=csaf.title,
        publisher=csaf_publisher,
        tracking=csaf_tracking,
        distribution=csaf_distribution,
    )

    csaf_root = CSAFRoot(
        document=csaf_document,
        product_tree=None,
        vulnerabilities=[],
    )

    return csaf_root


def _get_document_id(document_id_prefix: str, document_base_id: str, document_version: int) -> str:
    return document_id_prefix + "_" + document_base_id + f"_{document_version:04d}"
