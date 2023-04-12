import csv
from datetime import datetime
from typing import Any

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font

from application.core.models import Observation, Product


def export_observations_excel(product: Product, status: str = None) -> Workbook:
    workbook = Workbook()
    workbook.iso_dates = True
    worksheet = workbook.active
    worksheet.title = "Observations"

    font_bold = Font(bold=True)

    row_num = 1

    if status:
        observations = Observation.objects.filter(
            product=product, current_status=status
        )
    else:
        observations = Observation.objects.filter(product=product)

    for observation in observations:
        if row_num == 1:
            col_num = 1
            for key in dir(observation):
                if (
                    key not in __get_excludes()
                    and not callable(getattr(observation, key))
                    and not key.startswith("_")
                ):
                    cell = worksheet.cell(row=row_num, column=col_num, value=key)
                    cell.font = font_bold
                    col_num += 1
            cell.font = font_bold
            row_num = 2
        if row_num > 1:
            col_num = 1
            for key in dir(observation):
                if (
                    key not in __get_excludes()
                    and not callable(getattr(observation, key))
                    and not key.startswith("_")
                ):
                    value = observation.__dict__.get(key)
                    if key in __get_foreign_keys() and getattr(observation, key):
                        value = str(getattr(observation, key))
                    if value and isinstance(value, datetime):
                        value = value.replace(tzinfo=None)
                    worksheet.cell(row=row_num, column=col_num, value=value)
                    col_num += 1
        row_num += 1

    return workbook


def export_observations_csv(
    response: HttpResponse, product: Product, status: str = None
) -> None:
    writer = csv.writer(  # nosemgrep: python.lang.security.use-defusedcsv.use-defusedcsv
        response
    )
    # Ony a closed user group can import observations, risk is accepted

    first_row = True

    if status:
        observations = Observation.objects.filter(
            product=product, current_status=status
        )
    else:
        observations = Observation.objects.filter(product=product)

    for observation in observations:
        fields: list[Any] = []
        if first_row:
            for key in dir(observation):
                if (
                    key not in __get_excludes()
                    and not callable(getattr(observation, key))
                    and not key.startswith("_")
                ):
                    fields.append(key)

            writer.writerow(fields)

            first_row = False
        if not first_row:
            for key in dir(observation):
                if (
                    key not in __get_excludes()
                    and not callable(getattr(observation, key))
                    and not key.startswith("_")
                ):
                    value = observation.__dict__.get(key)
                    if key in __get_foreign_keys() and getattr(observation, key):
                        value = str(getattr(observation, key))
                    if value and isinstance(value, str):
                        value = value.replace("\n", " NEWLINE ").replace("\r", "")
                    fields.append(value)

            writer.writerow(fields)


def __get_excludes():
    return [
        "identity_hash",
        "pk",
        "objects",
        "unsaved_references",
        "unsaved_evidences",
        "NUMERICAL_SEVERITIES",
        "SEVERITY_CHOICES",
        "SEVERITY_CRITICAL",
        "SEVERITY_HIGH",
        "SEVERITY_LOW",
        "SEVERITY_MEDIUM",
        "SEVERITY_NONE",
        "SEVERITY_UNKOWN",
        "STATUS_CHOICES",
        "STATUS_DUPLICATE",
        "STATUS_FALSE_POSITIVE",
        "STATUS_IN_REVIEW",
        "STATUS_NOT_AFFECTED",
        "STATUS_OPEN",
        "STATUS_RESOLVED",
        "STATUS_RISK_ACCEPTED",
    ]


def __get_foreign_keys():
    return ["parser", "product"]
