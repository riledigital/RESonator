from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from resonator.RESonator import RESonator
from tempfile import NamedTemporaryFile, TemporaryDirectory

FOLDER_OUTPUT = "tests/jobs"
UPLOAD_FOLDER = "tests/uploads"
Path(FOLDER_OUTPUT).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "toml", "xml"}
app = Flask(__name__)

app.config["FOLDER_OUTPUT"] = FOLDER_OUTPUT
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "the random string"


@app.route("/")
def home():
    return render_template("index.jinja")


def validate_file(request, filename):
    # check if the post request has the file part
    if filename not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files[filename]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        save_temp_file(file, filename)
        return True


@app.route("/process-job", methods=["GET", "POST"])
def process_job():
    if request.method == "POST":
        for filename in ["filelms", "fileeval", "filemeta"]:
            validate_file(request, filename)
        output_filename = "test_job.xml"
        outfile = NamedTemporaryFile()
        RESonator.process_job(
            path_lms_in=session["filelms"],
            path_eval_in=session["fileeval"],
            path_metadata_in=session["filemeta"],
            path_final_out=Path(app.config["FOLDER_OUTPUT"]) / output_filename,
        )
        return redirect(url_for("download_file", name=output_filename))
    return render_template("process-job.jinja")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploads/<name>")
def download_file(name):
    uploads = Path(app.config["UPLOAD_FOLDER"])
    return send_from_directory(uploads.absolute, name)


if __name__ == "__main__":
    app.run(ssl_context="adhoc")


def save_temp_file(file, filename):
    """Temporarily save the file to session

    Args:
        file ([type]): [description]
        filename ([type]): [description]

    Returns:
        [type]: [description]
    """
    uploads = f'{Path(app.config["UPLOAD_FOLDER"]) / Path(filename)}{Path(file.filename).suffix}'
    file.save(uploads)
    session[filename] = Path(uploads)

    # filename = secure_filename(filename)
    # tempfile = NamedTemporaryFile()
    # file.save(tempfile)
    # session[filename] = tempfile
    # return tempfile
