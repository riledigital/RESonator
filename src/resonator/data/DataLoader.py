import pandas as pd
import re
import logging
from pathlib import Path


class DataLoader:
    """
    Handles file loading
    """

    def __init__(self):
        logging.info("DataLoader ready to read!")

    def load_file_disk(self, path_in):
        """
        loads a file from disk and outputs a pandas dataframe

        Args:
            path_in (Path): Path
        """
        data = pd.read_csv(path_in, encoding="utf8")
        return data

    def load_from_request(self):
        """TODO: Placeholder, load data from an HTTP request?"""
        print("Currently unimplemented")
        pass
