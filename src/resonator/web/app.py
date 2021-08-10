from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    send_file,
)
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from resonator.RESonator import RESonator
from tempfile import NamedTemporaryFile, TemporaryDirectory, tempdir
from webbrowser import open as open_browser

FOLDER_OUTPUT = "tests/jobs"
UPLOAD_FOLDER = "tests/uploads"

# Setup files
def setup_folders(files: list):
    for file in files:
        Path(file).mkdir(parents=True, exist_ok=True)


setup_folders([FOLDER_OUTPUT, UPLOAD_FOLDER])

ALLOWED_EXTENSIONS = {"csv", "xlsx", "toml", "xml"}
app = Flask(__name__)

app.config["FOLDER_OUTPUT"] = FOLDER_OUTPUT
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "the random string"


@app.route("/")
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


@app.route("/process-job", methods=["GET", "POST"])
def process_job():
    if request.method == "POST":
        for file_expected in ["filelms", "fileeval", "filemeta"]:
            validate_file(request, file_expected)
        output_filename = "test_job.xml"
        tempfile = NamedTemporaryFile()
        path_final_out = Path(app.config["FOLDER_OUTPUT"]) / output_filename
        xml_string = RESonator.process_job(
            path_lms_in=Path(session["filelms"]),
            path_eval_in=Path(session["fileeval"]),
            path_metadata_in=Path(session["filemeta"]),
            path_final_out=Path(tempfile.name),
        )
        # Ideally return the xml, an output name, the path to the output, all in one tuple.
        return send_from_directory(
            Path(app.config["FOLDER_OUTPUT"]).absolute(),
            output_filename,
            attachment_filename=output_filename,
            as_attachment=True,
            download_name=output_filename,
            max_age=0,
            mimetype="application/xml",
        )
        # return redirect(url_for("download_file", name=output_filename))
    else:
        return render_template("process-job.jinja")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/output/<name>")
def download_file(name):
    outputs = Path(app.config["FOLDER_OUTPUT"])
    return send_from_directory(outputs.absolute, name)


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
    uploads = f'{Path(app.config["UPLOAD_FOLDER"]) / Path(filename)}{Path(file.filename).suffix}'
    file.save(uploads)
    session[filename] = uploads
    # tempfile = NamedTemporaryFile()
    # file.save(tempfile)
    # session[filename] = tempfile
    # return tempfile


HOSTNAME = "0.0.0.0"
PORT = 5000
import logging

if __name__ == "__main__":
    connection_str = f"https://localhost:{PORT}"
    open_browser(connection_str)
    app.run(ssl_context="adhoc", host=HOSTNAME, port=PORT)
    print(f"Opening your browser to: {connection_str}")
