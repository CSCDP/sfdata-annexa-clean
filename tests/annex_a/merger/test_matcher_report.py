import unittest
from sfdata_annexa_clean.annex_a.merger import configuration
from sfdata_annexa_clean.annex_a.merger.matcher_report import column_report, process_report, parse_report
from sfdata_annexa_clean.config import Config
from tests.configuration import PROJECT_ROOT


class TestMatcherReport(unittest.TestCase):

    def test_parse_and_process(self):
        """
        This is not a unit test - it tests the integration of multiple components
        """
        config = Config()

        records = parse_report(PROJECT_ROOT / "examples/matcher-report/report.xlsx")

        data_sources = configuration.parse_datasources(config['datasources'])

        sheet_with_headers, unmatched_list = process_report(records, data_sources)

        column_report(sheet_with_headers, unmatched_list, "test-report.xlsx")
