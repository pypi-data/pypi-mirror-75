import os

import xlsxwriter

from .commons import run_requests, structure_cardinality
from .consts import RED_TO_GREEN_GRADIENT
from ..services.services import Services


def convert_to_xlsx(
    input_path: str, services: Services, workers: int = 1, output_path: str = None,
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
        workers {int} -- Amount of multithread. (default: {3})
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

    write_single_cardinality(
        workbook,
        single_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    write_multi_cardinality(
        workbook,
        multi_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    if vat_validation_result:
        write_vat_validation(vat_validation_result, workbook)

    workbook.close()


def write_single_cardinality(
    workbook,
    single_cardinality: dict,
    bold_header,
    red_to_green_formats: list,
    default_cols,
    validation_endpoint,
):
    """Write single cardinality items to workbook.

    Arguments:
        workbook {[type]} -- [description]
        single_cardinality {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        non_validation_cols {[type]} -- [description]
    """
    worksheet = workbook.get_worksheet_by_name("single_cardinality")

    for idx, row in single_cardinality.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key, bold_header)
            column_value, probability, validation_errors = value

            if probability:
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


def write_multi_cardinality(
    workbook,
    multi_cardinality: dict,
    bold_header,
    red_to_green_formats: list,
    default_cols,
    validation_endpoint,
):
    """Write multi cardinality items to workbook.

    Arguments:
        workbook {[type]} -- [description]
        multi_cardinality {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        non_validation_cols {[type]} -- [description]
    """
    worksheet = workbook.get_worksheet_by_name("multi_cardinality")
    item_count = 1

    for idx, row in multi_cardinality.items():
        for row_number, row_item in row.items():
            count = 0
            for key, value in row_item.items():
                worksheet.write(0, count, key, bold_header)
                column_value, probability, validation_errors = value

                if probability:
                    color_idx = int((len(red_to_green_formats) - 1) * probability)
                    color = red_to_green_formats[color_idx]
                    worksheet.write(item_count, count, column_value, color)
                else:
                    worksheet.write(item_count, count, column_value)

                if validation_endpoint and key not in default_cols:
                    validation_errors = validation_errors if validation_errors else 0
                    count += 1
                    worksheet.write(0, count, f"{key}ValidationErrors", bold_header)
                    if validation_errors == 0:
                        worksheet.write(item_count, count, validation_errors)
                    else:
                        worksheet.write(item_count, count, len(validation_errors))
                        worksheet.write_comment(
                            item_count, count, str(validation_errors)
                        )

                count += 1
            item_count += 1


def write_vat_validation(result, workbook):
    workbook.add_worksheet("vat_validation")
    worksheet = workbook.get_worksheet_by_name("vat_validation")

    for idx, row in result.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key)
            worksheet.write(idx + 1, count, value)
            count += 1
