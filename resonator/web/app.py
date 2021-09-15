from flask import (
    after_this_request,
    Blueprint,
    current_app,
    Flask,
    flash,
    request,
    redirect,
    render_template,
    session,
    send_file,
)
from werkzeug.utils import secure_filename
from os import urandom, remove
from pathlib import Path
from resonator.RESonator import RESonator
from tempfile import NamedTemporaryFile, mkstemp
from webbrowser import open as open_browser
from importlib.metadata import version

resonator = Blueprint("resonator", __name__, template_folder="templates")
flask_tempfiles = []

VERSION = version("resonator")
ALLOWED_EXTENSIONS = {"csv", "xlsx", "toml", "xml"}


@resonator.route("/")
def home():
    return render_template("index.jinja", context={"version": VERSION})


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
        return file


@resonator.route("/validate-dtd", methods=["GET", "POST"])
def validate_dtd():
    """DTD validation route

    Returns:
        [type]: [description]
    """
    if request.method == "POST":
        # Get the POSTed form and validate it!
        file = validate_file(request, "fileresxml")
        filename = file.filename
        validation = RESonator.validate_file(session["fileresxml"])
        context = validation.copy()
        context["filename"] = filename
        return render_template("validate-result.jinja", context=context)
    elif request.method == "GET":
        return render_template("validate.jinja")


@resonator.route("/process-job", methods=["GET", "POST"])
def process_job():
    if request.method == "POST":
        for file_expected in ["filelms", "fileeval", "filemeta"]:
            validate_file(request, file_expected)
        output_filename = "test_job.xml"
        tempfile = NamedTemporaryFile(suffix=".xml")
        xml_string = RESonator.process_job(
            path_lms_in=Path(session["filelms"]),
            path_eval_in=Path(session["fileeval"]),
            path_metadata_in=Path(session["filemeta"]),
            path_final_out=Path(tempfile.name),
        )

        @after_this_request
        def cleanup(response):
            current_app.logger.info("Attempting cleanup...")
            cleanup_temp()
            return response

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
    for file_expected in session.keys():
        file = session[file_expected]
        current_app.logger.info(f"Deleting {file}")
        remove(file)
    current_app.logger.info(f"Clearing session.")
    session.clear()


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


@resonator.context_processor
def inject_version():
    return dict(version=VERSION)


HOSTNAME = "localhost"
# Use 0 for a dyanmic port
PORT = 0


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = urandom(24)
    app.logger.info(f"RESonator version {version('resonator')}")
    app.register_blueprint(resonator)
    return app


import socket


def find_empty_port():
    """find and return an empty port # to run the app on.

    Returns:
        string: port number
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


if __name__ == "__main__":
    if (PORT is None) or (PORT == 0):
        PORT = find_empty_port()
    connection_str = f"http://localhost:{PORT}"
    open_browser(connection_str)
    print(f"Dev server opening your browser to: {connection_str}")
    app = create_app()
    app.run(host=HOSTNAME, port=PORT)
