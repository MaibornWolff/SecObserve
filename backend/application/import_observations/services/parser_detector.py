from csv import DictReader
from io import StringIO
from json import load
from typing import Any, Optional

from django.core.files.base import File
from rest_framework.exceptions import ValidationError

from application.import_observations.exceptions import ParserError
from application.import_observations.models import Parser
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.services.parser_registry import (
    get_parser_class_from_parser_name,
)
from application.import_observations.types import Parser_Filetype, Parser_Source


def detect_parser(file: File) -> tuple[Parser, BaseFileParser, Any]:
    if file.name and not (
        file.name.endswith(".csv")
        or file.name.endswith(".json")
        or file.name.endswith(".sarif")
    ):
        raise ValidationError("File is not CSV, JSON or SARIF")

    if file.name and file.name.endswith(".csv"):
        try:
            content = file.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            reader = DictReader(StringIO(content), delimiter=",", quotechar='"')
        except Exception:
            raise ValidationError("File is not valid CSV")

        rows = []
        for row in reader:
            rows.append(row)

        parser, parser_instance = _get_parser(rows, Parser_Filetype.FILETYPE_CSV)
        if parser and parser_instance:
            return parser, parser_instance, rows

    if file.name and (file.name.endswith(".json") or file.name.endswith(".sarif")):
        try:
            data = load(file)
        except Exception:
            raise ValidationError("File is not valid JSON")

        if data:
            parser, parser_instance = _get_parser(data, Parser_Filetype.FILETYPE_JSON)
            if parser and parser_instance:
                return parser, parser_instance, data

    raise ValidationError("No suitable parser found")


def instanciate_parser(parser: Parser) -> BaseParser:
    parser_class = get_parser_class_from_parser_name(parser.name)
    if not parser_class:
        raise ParserError(f"Parser {parser.name} not found in parser registry")
    parser_instance: BaseParser = parser_class()
    return parser_instance


def _get_parser(
    data: Any, filetype: str
) -> tuple[Optional[Parser], Optional[BaseFileParser]]:
    parsers = Parser.objects.filter(source=Parser_Source.SOURCE_FILE).order_by("name")
    for parser in parsers:
        try:
            parser_instance = instanciate_parser(parser)
        except ModuleNotFoundError:
            continue

        if not isinstance(parser_instance, BaseFileParser):
            raise ParserError(f"{parser.name} isn't a file parser")

        if parser_instance.get_filetype() == filetype and parser_instance.check_format(
            data
        ):
            return parser, parser_instance

    return None, None
