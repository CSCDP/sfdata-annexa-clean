import logging
from pathlib import Path

import pandas as pd
from typing import Dict, Any


logger = logging.getLogger(__name__)


class ExcelFileSource:
    """
    A utility class for saving reloading of Excel files when reading multiple sheets
    """
    __file_map: Dict[Any, pd.ExcelFile] = dict()

    def get_file(self, filename: str) -> pd.ExcelFile:
        """
        Returns a cached or new ExcelFile if the filename has never been loaded before
        :param filename:
        :return:
        """
        if filename in self.__file_map:
            logger.debug(f"Fetching {filename} from cache.")
            return self.__file_map[filename]
        else:
            logger.debug(f"Creating new ExcelFile for {filename}.")

        file = filename

        if isinstance(file, str):
            file = Path(file)

        if not file.is_absolute():
            file = Path.cwd() / file

        return self.__file_map.setdefault(filename, pd.ExcelFile(file))
