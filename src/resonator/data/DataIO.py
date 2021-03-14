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
            my_meta = (
                pd.read_csv(
                    path_in,
                    skipinitialspace=True,
                    parse_dates=[
                        "class_startdate",
                        "class_enddate",
                        "class_starttime",
                        "class_endtime",
                    ],
                    infer_datetime_format=True,
                    # TODO: Note that meta has to be utf8
                    encoding="utf8",
                )
                .rename(columns=lambda x: x.strip())
                .rename(columns=lambda y: y.lower())
            )
            return my_meta.to_dict(orient="records")[0]
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

    def load_from_request(self):
        """TODO: Placeholder, load data from an HTTP request?"""
        print("Currently unimplemented")
        pass
