import os

from distutils.util import strtobool

import xlsxwriter
import pandas as pd
import numpy as np

from .commons import run_requests, structure_cardinality
from .consts import RED_TO_GREEN_GRADIENT
from ..services.services import Services


def convert_to_xlsx(
    input_path: str,
    services: Services,
    workers: int = 1,
    output_path: str = None,
    normalize: bool = None,
):
    """Sends requests to defined Hypatos services for every invoice found in given
    directory. Merges results off all services into one Excel file and writes to
    project directory. Every key, value pair from Invoice Extractor will flattened
    into the following tuple:

        key = (value, probability, validation[optional])

    Arguments:
        path {str} -- Path to the directory containing invoices, uses rglob.
        extractor_endpoint {str} -- Url of Hypatos extractor service.

    Keyword Arguments:
        vat_validator_endpoint {str} -- Url of vat_validator. (default: {None})
        validation_endpoint {str} -- Url of validation. (default: {None})
        token {str} -- API token. (default: {None})
        workers {int} -- Amount of multithread. (default: {1})
    """
    if not output_path:
        output_path = f"{os.path.normpath(input_path).split(os.path.sep)[-1]}.xlsx"
    else:
        output_path = f"{os.path.join(os.getcwd(), output_path)}"
        if not os.path.isdir(os.path.sep.join(output_path.split(os.path.sep)[:-1])):
            quit("Output directory does not exsist")

    # Get requests result
    (
        result,
        single_fieldnames,
        multi_fieldnames,
        default_cols,
        vat_validation_result,
    ) = run_requests(workers, input_path, services)

    # Structure result
    single_cardinality, multi_cardinality = structure_cardinality(
        result, single_fieldnames, multi_fieldnames
    )

    # Init workbook/sheets
    workbook = xlsxwriter.Workbook(output_path)
    workbook.add_worksheet("single_cardinality")
    workbook.add_worksheet("multi_cardinality")

    # Styling
    header = workbook.add_format({"bold": True})
    probability_format = [
        workbook.add_format({"bold": True, "bg_color": color})
        for color in RED_TO_GREEN_GRADIENT
    ]

    # Normalize probability
    if normalize and bool(strtobool(services.headers["probabilities"])):
        single_cardinality, multi_cardinality = (
            normalize_probability(single_cardinality),
            normalize_probability(multi_cardinality),
        )

    write_sheet(
        workbook.get_worksheet_by_name("single_cardinality"),
        single_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    write_sheet(
        workbook.get_worksheet_by_name("multi_cardinality"),
        multi_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    if vat_validation_result:
        write_vat_validation(vat_validation_result, workbook)

    workbook.close()


def write_sheet(
    worksheet,
    invoices: list,
    bold_header,
    red_to_green_formats: list,
    default_cols,
    validation_endpoint,
):
    """Write items to workbook sheet.

    Arguments:
        worksheet {[type]} -- [description]
        invoices {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        non_validation_cols {[type]} -- [description]
    """
    for idx, row in enumerate(invoices):
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key, bold_header)
            column_value, probability, validation_errors = value

            if pd.notna(probability):
                color_idx = int((len(red_to_green_formats) - 1) * probability)
                color = red_to_green_formats[color_idx]
                worksheet.write(idx + 1, count, column_value, color)
            else:
                worksheet.write(idx + 1, count, column_value)

            if validation_endpoint and key not in default_cols:
                validation_errors = validation_errors if validation_errors else 0
                count += 1
                worksheet.write(0, count, f"{key}ValidationErrors", bold_header)
                if validation_errors == 0:
                    worksheet.write(idx + 1, count, validation_errors)
                else:
                    worksheet.write(idx + 1, count, len(validation_errors))
                    worksheet.write_comment(idx + 1, count, str(validation_errors))

            count += 1

    for i, width in enumerate(get_col_widths(pd.DataFrame.from_records(invoices))):
        worksheet.set_column(i, i, width)


def get_col_widths(invoices):
    return [
        min(max([len(str(s[0])) for s in invoices[col].values] + [len(col)]), 70)
        for col in invoices.columns
    ]


def write_vat_validation(result, workbook):
    workbook.add_worksheet("vat_validation")
    worksheet = workbook.get_worksheet_by_name("vat_validation")

    for idx, row in result.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key)
            worksheet.write(idx + 1, count, value)
            count += 1


def normalize_probability(invoices: list):
    """ Normalize the probabilities for every column inbetween range(min, max) of
    particulair column.

    Args:
        invoices ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Read
    probabilities = {}
    for idx, invoice in enumerate(invoices):
        probabilities[idx] = {k: v[1] for k, v in invoice.items()}

    # Normalize
    df = pd.DataFrame.from_dict(probabilities, orient="index")
    for col in df.columns:
        if not df[col].isnull().all():
            min_value, max_value = (
                df[col].min(),
                df[col].max(),
            )
            if min_value == max_value:
                df[col] = pd.Series([np.nan] * len(df[col]))
            else:
                df[col] = (df[col] - min_value) / (max_value - min_value)

    # Write
    normalized = df.to_dict("records")
    for idx, invoice in enumerate(invoices.copy()):
        for col in invoice:
            if invoice[col]:
                triplet = list(invoices[idx][col])
                triplet[1] = normalized[idx][col]
                invoices[idx][col] = triplet

    return invoices
