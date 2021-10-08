import logging
import argparse
from pathlib import Path

from sfdata_annexa_clean.annex_a.cleaner import clean
from sfdata_annexa_clean.annex_a.custom_cleaner import custom_clean
from sfdata_annexa_clean.annex_a.merger import configuration, find_sources, merge_dataframes

from sfdata_annexa_clean.config import Config

logger = logging.getLogger()

MERGED_FILE = Path("merged.xlsx")
MATCHING_FILE = Path("matching-report.xlsx")
OUTPUT_FILE = Path("cleaned.xlsx")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Merge and clean Annex A'
    )
    parser.add_argument("--merge", "-m", type=str, nargs="*", help="File locations to merge")
    parser.add_argument("--clean", "-c", type=str, nargs="?", help="Name of matching report")

    parser.add_argument("--data-sources", type=str, nargs="*", help="Datasource configuration file(s)",
                        default=['DEFAULT_DATA_SOURCES'])

    parser.add_argument("--data-map", type=str, nargs="*", help="Data map configuration file(s)",
                        default=['DEFAULT_DATA_MAP'])

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Configure Data Clean
    config = Config(*(args.data_sources + args.data_map))

    if args.merge:
        # Configure standard settings
        data_sources = configuration.parse_datasources(config['datasources'])
        sources = find_sources(args.merge, data_sources=data_sources)
        merge_dataframes(sources, data_sources=data_sources, output_file=MERGED_FILE)

        # Launch cleaning
        clean(**config, input_file=MERGED_FILE, matching_report_file=MATCHING_FILE, output_file=OUTPUT_FILE)

    if args.clean:
        custom_clean(**config, input_matching=MATCHING_FILE, output_file=OUTPUT_FILE)
