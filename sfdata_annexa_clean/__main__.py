import logging
import pandas as pd
import os, webbrowser, pathlib

from sfdata_annexa_clean.annex_a.cleaner import clean
from sfdata_annexa_clean.annex_a.custom_cleaner import custom_clean
from sfdata_annexa_clean.annex_a.merger import configuration, find_sources, read_sources, merge_dataframes
from sfdata_annexa_clean.annex_a.merger.file_scanner import ScanSource
import argparse

from sfdata_annexa_clean.config import Config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("This is just to get logging to work - it seems to refuse to log unless you log something!")

MERGED_FILE = pathlib.Path(os.path.abspath("merged.xlsx"))

def merge(input_files):
    # Configure standard settings
    data_sources = configuration.parse_datasources("config/annex-a-merge.yml")

    sources = find_sources(input_files, data_sources=data_sources)

    merge_dataframes(sources, data_sources=data_sources, output_file=MERGED_FILE)

    # webbrowser.open(MERGED_FILE.as_uri())


def _clean(matching_report=None):
    # Set paths

    config = Config("config/data-map.yml")

    # Full path to the input file that should be cleaned
    config["input_file"] = MERGED_FILE.as_uri()

    # Full path to the output file that will hold the cleaned data
    config["output_file"] = "cleaned.xlsx"

    # Full path to a file holding a report of how the matching was performed
    config["matching_report_file"] = "matching_report.xlsx"

    # Input matching
    if matching_report:
        config["input_matching"] = matching_report

    # Launch cleaning
    clean(**config)


def _custom_clean(input_matching):
    config = Config("config/data-map.yml")

    # Full path to the merged file that should be cleaned (the one from 10-MERGE)
    config['input_file'] = MERGED_FILE.as_uri()

    # Full path to the matching report you edited
    config['input_matching'] = input_matching

    # Full path to the output file that will hold the cleaned data
    config['output_file'] = "final_cleaned.xlsx"

    custom_clean(**config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Merge and clean Annex A'
    )
    parser.add_argument("--merge", "-m", type=str, nargs="*", help="File locations to merge")
    parser.add_argument("--clean", "-c", type=str, nargs="?", help="Name of matching report")

    args = parser.parse_args()
    if args.merge:
        merge(args.merge)
        _clean()

    if args.clean:
        _custom_clean(args.clean)

