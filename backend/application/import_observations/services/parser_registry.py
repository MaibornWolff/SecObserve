import importlib
import logging
from typing import Optional, Type

from application.core.models import Parser
from application.core.queries.parser import get_parser_by_name
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Source, Parser_Type

logger = logging.getLogger("secobserve.import_observations")


def register_parser(module_name: str, class_name: str) -> None:
    parser_class = get_parser_class_from_module_class_names(module_name, class_name)

    name = parser_class.get_name()
    my_type = parser_class.get_type()

    source = Parser_Source.SOURCE_UNKOWN
    for base in parser_class.__bases__:
        if base is BaseAPIParser:
            source = Parser_Source.SOURCE_API
            break
        if base is BaseFileParser:
            source = Parser_Source.SOURCE_FILE
            break

    parser = get_parser_by_name(name)
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
        if parser.module_name != module_name:
            parser.module_name = module_name
            changed = True
        if parser.class_name != class_name:
            parser.class_name = class_name
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
    module = importlib.import_module(
        f"application.import_observations.parsers.{module_name}.parser"
    )
    parser_class = getattr(module, class_name)

    if not issubclass(parser_class, BaseParser):
        raise Exception(  # pylint: disable=broad-exception-raised
            f"{class_name} is not a subclass of BaseParser"
        )

    return parser_class
