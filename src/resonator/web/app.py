from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.jinja")


@app.route("/process-job")
def process_job():
    return render_template("process-job.jinja")
