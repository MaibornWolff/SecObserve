import importlib
import logging
from typing import Optional, Type

from application.import_observations.models import Parser
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
    BaseParser,
)
from application.import_observations.queries.parser import (
    get_parser_by_module_and_class,
)
from application.import_observations.types import Parser_Source, Parser_Type

logger = logging.getLogger("secobserve.import_observations")


def register_parser(module_name: str, class_name: str) -> None:
    parser_class = get_parser_class_from_module_class_names(module_name, class_name)

    name = parser_class.get_name()
    my_type = parser_class.get_type()

    source = Parser_Source.SOURCE_OTHER
    for base in parser_class.__bases__:
        if base is BaseAPIParser:
            source = Parser_Source.SOURCE_API
            break
        if base is BaseFileParser:
            source = Parser_Source.SOURCE_FILE
            break

    parser = get_parser_by_module_and_class(module_name, class_name)
    if parser:
        changed = False
        if parser.name != name:
            parser.name = name
            changed = True
        if parser.type != my_type:
            parser.type = my_type
            changed = True
        if parser.source != source:
            parser.source = source
            changed = True
        if changed:
            parser.save()
    else:
        Parser(
            name=name,
            type=my_type,
            source=source,
            module_name=module_name,
            class_name=parser_class.__name__,
        ).save()


def create_manual_parser() -> None:
    try:
        Parser.objects.get(type=Parser_Type.TYPE_MANUAL)
    except Parser.DoesNotExist:
        Parser(
            name="Manual",
            source=Parser_Source.SOURCE_MANUAL,
            type=Parser_Type.TYPE_MANUAL,
        ).save()
    except Parser.MultipleObjectsReturned:
        # Delete all manual parsers except the first one
        first_parser = True
        for parser in Parser.objects.filter(type=Parser_Type.TYPE_MANUAL):
            if first_parser:
                first_parser = False
            else:
                parser.delete()


def get_parser_class_from_parser_name(name: str) -> Optional[Type[BaseParser]]:
    parser = Parser.objects.get(name=name)
    return get_parser_class_from_module_class_names(
        parser.module_name, parser.class_name
    )


def get_parser_class_from_module_class_names(
    module_name: str, class_name: str
) -> Type[BaseParser]:
    module = importlib.import_module(  # nosemgrep
        f"application.import_observations.parsers.{module_name}.parser"
    )
    # nosemgrep because of rule python.lang.security.audit.non-literal-import.non-literal-import
    # This is the price you pay for a dynamic parser registry. We accept the risk.

    parser_class = getattr(module, class_name)
    if not issubclass(parser_class, BaseParser):
        raise Exception(  # pylint: disable=broad-exception-raised
            f"{class_name} is not a subclass of BaseParser"
        )

    return parser_class
