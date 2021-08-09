from typing import Dict, TextIO
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path
import pytomlpp
from pprint import pformat


class DataIO:
    """
    Handles file loading
    """

    def __init__(self):
        logging.info("DataIO ready to read!")

    @classmethod
    def load_file_disk(cls, path_in: Path, meta: bool = False) -> pd.DataFrame:
        """loads a file from disk and outputs a pandas dataframe

        Args:
            path_in (Path): input file

        Raises:
            Exception:

        Returns:
            [type]: [description]
        """
        logging.info(f"Input file as {path_in} with extension {path_in.suffix}")
        if meta:
            meta_file = open(path_in, mode="r").read()
            my_meta = pytomlpp(meta_file)
            return my_meta
        if path_in.suffix == ".xlsx":
            dtypes_names = [
                "Q1",
                "Q2",
                "Q3_1",
                "Q3_2",
                "Q4_1",
                "Q4_2",
                "Q4_3",
                "Q4_4",
                "Q5_1",
                "Q5_2",
                "Q5_3",
                "Q5_4",
                "Q5_5",
                "Q5_6",
                "Q5_7",
                "Q5_8",
                "Q6_1",
                "Q6_2",
                "Q6_3",
                "Q6_4",
                "Q6_5",
                "Q7_1",
                "Q7_2",
                "Q7_3",
                "Q7_4",
                "Q8",
                "Q9",
                "Q10",
                "Q11",
            ]
            # Read Q/A columns as object
            dtype = {k: "object" for k in dtypes_names}
            data = pd.read_excel(
                path_in, header=0, skiprows=[1], dtype=dtype, sheet_name=0
            )
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
    def load_toml(cls, path_in: Path) -> Dict:
        with open(path_in, "r") as reader:
            logging.info(f"Loading toml: {path_in}")
            file_str = reader.read()
            toml = pytomlpp.loads(file_str)
            logging.info(f"Loaded toml: \n{pformat(toml)}")
            return toml

    @classmethod
    def write_output_file(cls, input_file: TextIO, path_out: Path) -> bool:
        with open(path_out, "w") as writer:
            writer.write(input_file)

    @classmethod
    def write_string_to_file(cls, input: str, path_out: Path) -> Path:
        with open(path_out, "w") as writer:
            writer.write(input)
            logging.info(f"Wrote XML output to {path_out}")
            return path_out

    @classmethod
    def load_from_request(cls):
        """TODO: Placeholder, load data from an HTTP request?"""
        print("Currently unimplemented")
        pass

    @classmethod
    def generate_filename(cls, path_in_meta: Path) -> str:
        meta = cls.load_toml(path_in_meta)
        course_number = meta.get("class_catalognum")
        date_formatted = datetime.today().strftime("%d%m%Y")
        trainingprovider_abbreviation = meta.get("trainingprovider_tpid", "NCDP")
        filename = (
            f"{trainingprovider_abbreviation}_{course_number}_{date_formatted}.XML"
        )

        def check_increment(test_path, acc):
            # Ignore increment if accumulator is 0
            increment = f"_{acc:02d}" if (acc >= 1) else ""
            filename = f"{trainingprovider_abbreviation}_{course_number}_{date_formatted}{increment}.XML"
            if Path.exists(filename):
                acc += 1
                check_increment(test_path, acc=acc)
            else:
                return filename

        final_out = check_increment(filename, 0)
        return final_out
