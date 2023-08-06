import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from copy import copy

import click
from filetype import guess

from ..services.requests import extract_invoice, validation, validate_vat


def run_requests(workers: int, path: str, services) -> dict:
    single_fieldnames = {
        "file_name": (None, None, None),
        "error_message": (None, None, None),
    }
    multi_fieldnames = {
        "file_name": (None, None, None),
        "row_number": (None, None, None),
    }
    default_cols = set().union(single_fieldnames.keys(), multi_fieldnames.keys())
    files = get_filenames(path)
    result, vat_validation_result = {}, {}

    with ThreadPoolExecutor(max_workers=workers) as exe:
        jobs = {
            exe.submit(
                extract_invoice,
                read_pdf(file_path),
                services.extractor_endpoint,
                file_extension,
                services.token,
                services.headers,
            ): file_path
            for file_path, file_extension in files.items()
        }
        label = f"Converting {len(jobs)} invoices"

        with click.progressbar(jobs, label=label) as bar:
            for idx, future in enumerate(as_completed(jobs)):
                file_name = jobs[future].split("/")[-1]
                validated_invoice = None

                try:
                    extracted_invoice = future.result(timeout=300)

                    if getattr(services, "validation_endpoint", None):
                        validated_invoice = validation(
                            extracted_invoice, services.validation_endpoint
                        )

                    if getattr(services, "vat_validation_endpoint", None):
                        vat_validation_result[idx] = validate_vat(
                            extracted_invoice, services.vat_validation_endpoint
                        )
                        vat_validation_result[idx]["file_name"] = file_name

                    result[idx] = flatten_invoice(extracted_invoice, validated_invoice,)
                except Exception as e:
                    result[idx] = {"error_message": (repr(e), None, None)}
                finally:
                    result[idx]["file_name"] = (file_name, None, None)

                collect_column_names(result[idx], single_fieldnames, multi_fieldnames)
                bar.update(1)

    if not result:
        quit(f"No files found in path")
    return (
        result,
        single_fieldnames,
        multi_fieldnames,
        default_cols,
        vat_validation_result,
    )


def flatten_invoice(invoice, validation):
    return_dict = dict()
    entities = invoice["entities"]
    probabilities = invoice.get("probabilities")

    def traverse_items(entities, probabilities, validation, _dict, *prefix):
        for k, v in entities.items():
            if isinstance(v, dict):
                traverse_items(
                    entities[k],
                    probabilities[k] if probabilities else None,
                    validation[k][0] if validation and k in validation else None,
                    return_dict,
                    k,
                )
            elif isinstance(v, list):
                # items, taxes, terms
                if all(isinstance(list_item, dict) for list_item in v):
                    for counter, list_item in enumerate(v):
                        temp_dict = {}
                        for item, value in list_item.items():
                            temp_dict[f"{k}_{item}_{counter}"] = value
                        traverse_items(
                            temp_dict,
                            probabilities[k][counter] if probabilities else None,
                            validation[k][0][str(counter)][0]
                            if validation
                            and k in validation
                            and str(counter) in validation[k][0]
                            else None,
                            return_dict,
                        )
                # ibanAll enc
                elif all(isinstance(list_item, str) for list_item in v):
                    for counter, list_item in enumerate(v):
                        _dict[f"{k}_{counter+1}_idx"] = (list_item, None, None)
                # Undefined datastructure
                else:
                    pass
            else:
                try:
                    # dirty solution, assumes no invoice extractor response field got underscore
                    original_k = k.split("_")[-2]
                except IndexError:
                    original_k = k

                if prefix:
                    field_name = f"{prefix[0]}_{k}"
                else:
                    field_name = k

                if probabilities and original_k in probabilities:
                    if probabilities[original_k]:
                        _dict[field_name] = (v, probabilities[original_k], None)
                    else:
                        _dict[field_name] = (v, None, None)
                else:
                    _dict[field_name] = (v, None, None)
                if validation:
                    if original_k in validation:
                        _dict[field_name] = (v, None, validation[original_k])

    traverse_items(entities, probabilities, validation, return_dict)
    return return_dict


def collect_column_names(
    extracted_doc: dict, single_fieldnames: dict, multi_fieldnames: dict
):
    """Iterate through extracted invoice and write fieldnames to single or multi
    cardinality

    Arguments:
        extracted_invoice {[type]} -- [description]
        multi_fieldnames {[type]} -- [description]
        single_fieldnames {[type]} -- [description]
    """
    for col_name in extracted_doc.keys():
        if col_name[-1].isdigit():
            label = "_".join(col_name.split("_")[:-1])
            multi_fieldnames[label] = (None, None, None)
        else:
            single_fieldnames[col_name] = (None, None, None)


def read_pdf(pdf_path: str) -> bytes:
    with open(pdf_path, "rb") as pdf:
        pdf = pdf.read()

    return pdf


def get_filenames(path: str) -> list:
    types = ("*.pdf", "*.tif", "*.tiff", "*.png", "*.jpg")
    abs_path = os.path.join(os.getcwd(), path)
    files_grabbed = []

    for files in types:
        files_grabbed.extend(Path(abs_path).rglob(files))
        files_grabbed.extend(Path(abs_path).rglob(files.upper()))

    files_grabbed = [str(f) for f in files_grabbed]
    return {f: guess(f).mime for f in files_grabbed if guess(f).mime}


def structure_cardinality(
    result: dict, single_fieldnames: dict, multi_fieldnames: dict
):
    """Structure the extracted invoice in different cardinalities.

    Arguments:
        result {[type]} -- [description]
        single_fieldnames {[type]} -- [description]
        multi_fieldnames {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    single_cardinality = []
    multi_cardinality = []

    for idx, document in result.items():
        single_item = copy(single_fieldnames)
        multi_items = {}

        for col, value in document.items():
            if col[-1].isdigit():
                num = int(col.split("_")[-1]) + 1
                label = "_".join(col.split("_")[:-1])
                if num not in multi_items:
                    multi_item = copy(multi_fieldnames)
                    multi_item["file_name"] = document["file_name"]
                    multi_item["row_number"] = (num, None, None)
                    multi_items[num] = multi_item

                multi_items[num][label] = document[col]
            else:
                single_item[col] = document[col]

        single_cardinality.append(single_item)
        multi_cardinality += [value for value in multi_items.values()]

    return single_cardinality, multi_cardinality
