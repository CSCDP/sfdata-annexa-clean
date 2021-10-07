import logging
import pandas as pd
from sfdata_annexa_clean.annex_a.merger.workbook_util import WorkSheetDetail
from sfdata_annexa_clean.datatables.cache import ExcelFileSource

logger = logging.getLogger(__name__)


def load_dataframe(
        source: WorkSheetDetail,
        file_source: ExcelFileSource = ExcelFileSource(),
) -> pd.DataFrame:

    logger.info(f"Reading '{source.sheetname}' from '{source.filename}' starting on row {source.header_row_index}")

    file = file_source.get_file(source.filename)
    df = pd.read_excel(file, skiprows=source.header_row_index - 1, sheet_name=source.sheetname)

    logger.debug(f"Read {df.shape[0]} rows and {df.shape[1]} cols from '{source.sheetname}' in '{source.filename}'")

    return df
