import pandas as pd
import re
import logging
from pathlib import Path


class DataIO:
    """
    Handles file loading
    """

    def __init__(self):
        logging.info("DataIO ready to read!")

    def load_file_disk(self, path_in: Path):
        """loads a file from disk and outputs a pandas dataframe

        Args:
            path_in (Path): input file

        Raises:
            Exception:

        Returns:
            [type]: [description]
        """
        logging.debug(f"Input file as {path_in} with extension {path_in.suffix}")
        if path_in.suffix == ".xlsx":
            data = pd.read_excel(path_in)
            return data
        elif path_in.suffix == ".csv":
            data = pd.read_csv(path_in, encoding="utf8")
            return data
        else:
            raise ValueError(
                f"Input file isn't csv or xslx. Please check input for: {path_in}"
            )

    def load_from_request(self):
        """TODO: Placeholder, load data from an HTTP request?"""
        print("Currently unimplemented")
        pass
