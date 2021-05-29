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
        data_lms = dataprep.prep_data_lms(input_lms, [], [])
        data_eval = dataprep.prep_data_eval(input_eval)

        outfile = XMLGenerator.XMLGenerator.generate_full_submission(
            data_eval, data_lms, input_metadata
        )

        DataIO.DataIO.write_output_file(outfile, path_final_out)
        return outfile

        return outfile
