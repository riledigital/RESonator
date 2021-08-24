from flask import (
    Blueprint,
    current_app,
    Flask,
    flash,
    request,
    redirect,
    render_template,
    session,
    send_from_directory,
    send_file,
)
from werkzeug.utils import secure_filename
from os import urandom, remove
from pathlib import Path
from resonator.RESonator import RESonator
from tempfile import NamedTemporaryFile, mkstemp
from webbrowser import open as open_browser

FOLDER_OUTPUT = "../../tests/jobs"
UPLOAD_FOLDER = "../../tests/uploads"

resonator = Blueprint("resonator", __name__, template_folder="templates")
flask_tempfiles = []

ALLOWED_EXTENSIONS = {"csv", "xlsx", "toml", "xml"}


@resonator.route("/")
def home():
    return render_template("index.jinja")


def validate_file(request, file_expected):
    # check if the post request has the file part
    if file_expected not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files[file_expected]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        save_temp_file(file, file_expected)
        return True


@resonator.route("/process-job", methods=["GET", "POST"])
def process_job():
    if request.method == "POST":
        for file_expected in ["filelms", "fileeval", "filemeta"]:
            validate_file(request, file_expected)
        output_filename = "test_job.xml"
        tempfile = NamedTemporaryFile(suffix=".xml")
        path_final_out = Path(current_app.config["FOLDER_OUTPUT"]) / output_filename
        xml_string = RESonator.process_job(
            path_lms_in=Path(session["filelms"]),
            path_eval_in=Path(session["fileeval"]),
            path_metadata_in=Path(session["filemeta"]),
            path_final_out=Path(tempfile.name),
        )
        # Ideally return the xml, an output name, the path to the output, all in one tuple.
        return send_file(
            tempfile.name,
            attachment_filename=output_filename,
            as_attachment=True,
            download_name=output_filename,
            max_age=0,
            mimetype="application/xml",
        )
    else:
        return render_template("process-job.jinja")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_temp():
    """Cleanup all temp files"""
    for file_expected in ["filelms", "fileeval", "filemeta"]:
        file = session[file_expected]
        current_app.logger.info(f"Deleting {file}")
        remove(file)


def save_temp_file(file, filename):
    """Temporarily save the file to session

    Args:
        file ([type]): [description]
        filename ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Sanitize filename for safety
    filename = secure_filename(filename)
    # Create an upload path
    # uploads = f'{Path(current_app.config["UPLOAD_FOLDER"]) / Path(filename)}{Path(file.filename).suffix}'
    # file.save(uploads)
    # session[filename] = uploads
    tempfile = NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix)
    # tempfilehandle, filepath = mkstemp()
    file.save(tempfile)
    session[filename] = tempfile.name
    return tempfile


# @resonator.teardown_request
# def teardown_request_func(error=None):

#     """
#     This function will run after a request, regardless if an exception occurs or not.
#     It's a good place to do some cleanup, such as closing any database connections.
#     If an exception is raised, it will be passed to the function.
#     You should so everything in your power to ensure this function does not fail, so
#     liberal use of try/except blocks is recommended.
#     """

#     current_app.logger.info("teardown_request is running!")
#     try:
#         cleanup_temp()
#     except error:
#         current_app.logger.info(error)
#     if error:
#         # Log the error
#         print(str(error))


HOSTNAME = "localhost"
PORT = 5000


def create_app():
    app = Flask(__name__)
    app.config["FOLDER_OUTPUT"] = FOLDER_OUTPUT
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = urandom(24)

    app.register_blueprint(resonator)
    return app


if __name__ == "__main__":
    connection_str = f"http://localhost:{PORT}"
    open_browser(connection_str)
    print(f"Dev server opening your browser to: {connection_str}")
    app = create_app()
    app.run(host=HOSTNAME, port=PORT)
