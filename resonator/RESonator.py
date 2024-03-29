from resonator.data import XMLGenerator, DataIO, DataPrep
from pathlib import Path
import logging
from lxml import etree


class RESonator:
    """Main class for app."""

    def __init__(self, path_lms_in, path_metadata_in, path_eval_in, path_final_out):
        logging.info("Processing job...")
        self.process_job(path_lms_in, path_metadata_in, path_eval_in, path_final_out)

    @classmethod
    def validate_file(cls, path_test_file: Path) -> bool:
        """validate input XML against the submission DTD

        Args:
            path_test_file (pathlib.Path): Path to submission DTD
        """
        test_submission = etree.parse(path_test_file)
        return XMLGenerator.XMLGenerator.validate_dtd(test_submission)

    @classmethod
    def process_job(cls, path_lms_in, path_metadata_in, path_eval_in, path_final_out):
        """Run a RES job.

        Args:
            path_lms_in ([type]): [description]
            path_metadata_in ([type]): [description]
            path_eval_in ([type]): [description]
            path_final_out ([type]): [description]

        Returns:
            [type]: [description]
        """
        inputs = DataIO.DataIO()
        input_lms = inputs.load_file_disk(path_lms_in, meta=False)
        input_metadata = inputs.load_toml(path_metadata_in)
        input_eval = inputs.load_file_disk(path_eval_in)

        dataprep = DataPrep.DataPrep()

        course_codes: list = input_metadata.get("codes")
        remove_users: list = input_metadata.get("remove_users")
        if course_codes == None:
            logging.warning(
                f"No course codes specified. Running job without filtering for courses."
            )

        if remove_users == None:
            logging.warning(
                f"No remove_users specified. Running job without removing any users from LMS set"
            )

        data_lms = dataprep.prep_data_lms(
            input_lms,
            course_codes,
            remove_users,
        )
        data_eval = dataprep.prep_data_eval(input_eval)

        xml_string = XMLGenerator.XMLGenerator.generate_full_submission(
            data_eval, data_lms, input_metadata
        )

        DataIO.DataIO.write_string_to_file(xml_string, path_final_out)
        return xml_string
