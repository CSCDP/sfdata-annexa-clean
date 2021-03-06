import logging
from dataclasses import dataclass, asdict
from typing import List, Any

from sfdata_annexa_clean.annex_a.merger.file_scanner import FileSource
from sfdata_annexa_clean.datatables.cache import ExcelFileSource

logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=True)
class WorkSheetHeaderItem:
    value: Any
    column_index: int


@dataclass(frozen=True, eq=True)
class WorkSheetDetail(FileSource):
    sheetname: str = None
    header_row_index: int = 1
    headers: List[WorkSheetHeaderItem] = None

    def header_names(self) -> List[str]:
        return [c.value for c in self.headers]


def find_worksheets(source: FileSource, file_source: ExcelFileSource = ExcelFileSource()) -> List[WorkSheetDetail]:

    data_sources = []  # type: List[WorkSheetDetail]

    logger.debug("Opening {}".format(source.filename))
    excel_file = file_source.get_file(source.filename)
    workbook = excel_file.book

    # try:
    #     workbook.sheetnames
    # except AttributeError:
    #     logger.warning("Skipping old excel file")
    #     return []

    for sheet_name in excel_file.sheet_names:
        logger.debug("Checking sheet {} in {}".format(sheet_name, source.filename))
        sheet = workbook[sheet_name]

        # We search for first row with more than 3 non-null values
        header_row_index = 1
        header_values = []  # type: List[WorkSheetHeaderItem]

        try:
            rows = sheet.rows
        except AttributeError:
            rows = [sheet[r] for r in range(sheet.nrows)]

        for ix, row in enumerate(rows):
            row_length = 0
            for col in row:
                if col.value is not None and len(str(col.value).strip()) > 0:
                    header_row_index = ix + 1
                    row_length += 1
            if row_length > 3:
                header_values = [WorkSheetHeaderItem(value=col.value, column_index=ix) for ix, col in enumerate(row)]
                break

        source_info = WorkSheetDetail(
            **asdict(source),
            sheetname=sheet_name,
            header_row_index=header_row_index,
            headers=header_values,
        )

        data_sources.append(source_info)

    return data_sources
