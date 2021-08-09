from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from pathlib import Path

UPLOAD_FOLDER = "tests/uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx", "toml", "xml"}

app = Flask(__name__)
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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print(filename)
        return True


@app.route("/process-job", methods=["GET", "POST"])
def process_job():
    if request.method == "POST":
        for filename in ["filelms", "fileeval", "filemeta"]:
            validate_file(request, filename)
            return redirect(url_for("download_file", name=filename))
    return render_template("process-job.jinja")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploads/<name>")
def download_file(name):
    uploads = Path(app.config["UPLOAD_FOLDER"])
    return send_from_directory(uploads.absolute, name)
