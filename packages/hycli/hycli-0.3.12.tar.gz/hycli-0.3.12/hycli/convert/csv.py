import os
import csv
from operator import itemgetter
from copy import deepcopy

from .commons import run_requests, structure_cardinality
from ..services.services import Services


def convert_to_csv(
    input_path: str,
    services: Services,
    workers: int = 1,
    output_path: str = None,
    probability=False,
):
    # Get requests result
    result, single_fieldnames, multi_fieldnames, default_cols, _ = run_requests(
        workers, input_path, services
    )
    # fieldnames = set().union(single_fieldnames, multi_fieldnames)
    processed_dir_name = os.path.normpath(output_path).split(os.path.sep)[-1]

    # Structure result
    single_cardinality, multi_cardinality = structure_cardinality(
        result, single_fieldnames, multi_fieldnames
    )

    structure_result(single_cardinality)

    with open(f"{processed_dir_name}_single_cardinality.csv", mode="w") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=sorted(single_fieldnames, key=itemgetter(0, -1)),
            extrasaction="ignore",
            delimiter=";",
        )
        writer.writeheader()
        for row in single_cardinality:
            writer.writerow(single_cardinality[row])


def structure_result(result):
    for row, row_items in deepcopy(result).items():
        for field, value in row_items.items():
            result[row][field] = value[0]
