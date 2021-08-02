from resonator.data import XMLGenerator, DataIO, DataPrep
import logging


class RESonator:
    """Main class for Resonator"""

    def __init__(
        self, path_lms_in, path_metadata_in, path_eval_in, path_final_out
    ) -> None:
        logging.info("Processing job...")
        return self.process_job(
            path_lms_in, path_metadata_in, path_eval_in, path_final_out
        )

    def process_job(self, path_lms_in, path_metadata_in, path_eval_in, path_final_out):
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
