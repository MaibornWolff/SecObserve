import logging
from typing import Optional, Type

from application.commons.services.log_message import format_log_message
from application.core.models import Parser
from application.core.queries.parser import get_parser_by_name
from application.import_observations.parsers.base_parser import (
    BaseAPIParser,
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Source, Parser_Type

logger = logging.getLogger("secobserve.import_observations")

SCANNERS = {}


def register_parser(parser_class: Type[BaseParser]) -> None:
    if not issubclass(parser_class, BaseParser):
        logger.warning(
            format_log_message(
                message=f'Class {parser_class.__name__} is not a subclass of BaseParser"'
            )
        )
        return

    name = parser_class.get_name()
    my_type = parser_class.get_type()

    SCANNERS[name] = parser_class

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
        if parser.name != name:
            parser.name = name
            parser.save()
        if parser.type != my_type:
            parser.type = my_type
            parser.save()
        if parser.source != source:
            parser.source = source
            parser.save()
    else:
        Parser(name=name, type=my_type, source=source).save()


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


def get_parser_class(name: str) -> Optional[Type[BaseParser]]:
    return SCANNERS.get(name)
