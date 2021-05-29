from typing import TextIO
import pandas as pd
import re
import logging
from pathlib import Path
import pytomlpp


class DataIO:
    """
    Handles file loading
    """

    def __init__(self):
        logging.info("DataIO ready to read!")

    @classmethod
    def load_file_disk(self, path_in: Path, meta: bool = False) -> pd.DataFrame:
        """loads a file from disk and outputs a pandas dataframe

        Args:
            path_in (Path): input file

        Raises:
            Exception:

        Returns:
            [type]: [description]
        """
        logging.debug(f"Input file as {path_in} with extension {path_in.suffix}")
        if meta:
            meta_file = open(path_in, mode="r").read()
            my_meta = parse_toml(meta_file)
            return my_meta
        if path_in.suffix == ".xlsx":
            data = pd.read_excel(path_in, header=0, skiprows=1)
            logging.debug(data.columns)
            return data
        elif path_in.suffix == ".csv":
            data = pd.read_csv(path_in, encoding="utf8")
            logging.debug(data.columns)
            return data
        else:
            raise ValueError(
                f"Input file isn't csv or xslx. Please check input for: {path_in}"
            )

    @classmethod
    def load_toml(self, path_in: Path):
        with open(path_in, "r") as reader:
            logging.info(f"Loading toml: {path_in}")
            toml = pytomlpp.loads(reader.read())
            logging.info(f"Loaded toml: \n{toml}")
            return toml

    @classmethod
    def write_output_file(clas, input_file: TextIO, path_out: Path) -> bool:
        with open(path_out, "w") as writer:
            writer.write(input_file)

    @classmethod
    def load_from_request(self):
        """TODO: Placeholder, load data from an HTTP request?"""
        print("Currently unimplemented")
        pass
