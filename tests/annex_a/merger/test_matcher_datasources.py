import unittest

from sfdata_annexa_clean.annex_a.merger import matcher
from sfdata_annexa_clean.annex_a.merger.matcher import match_data_sources, MatchedSheet
from sfdata_annexa_clean.annex_a.merger.configuration import SourceConfig
from sfdata_annexa_clean.annex_a.merger.workbook_util import WorkSheetDetail

class TestMatcher(unittest.TestCase):

    def test_datasource_matcher(self):
        sheet_detail_list = [
            WorkSheetDetail(filename="File 1", sheetname="List 1"),
            WorkSheetDetail(filename="File 2", sheetname="List 2"),
        ]
        source_configuration_list = [
            SourceConfig(name="list 1"),
            SourceConfig(name="list 3")
        ]

        expected_log_name = matcher.__name__

        with self.assertLogs(expected_log_name.split('.')[0], level='INFO') as logs:
            matched, unmatched = match_data_sources(sheet_detail_list, source_configuration_list)

        self.assertEqual(matched, [
            MatchedSheet(sheet_detail=sheet_detail_list[0], source_config=source_configuration_list[0])
        ])

        self.assertEqual(logs.output,
                         [f"WARNING:{expected_log_name}:No datasource identified for " +
                          "'List 2' in 'File 2'"]
                         )
