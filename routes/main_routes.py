import os

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

from simulator.runner import run_experiment


main = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
	return render_template("index.html")


@main.route("/run", methods=["POST"])
def run() -> str:
	dataset_file = request.files.get("dataset")
	task_count = request.form.get("task_count", type=int)
	algorithms = request.form.getlist("algorithms")

	if dataset_file is None or dataset_file.filename == "":
		return render_template(
			"results.html",
			results={"error": "Please upload a dataset file."},
		)

	upload_folder = current_app.config["UPLOAD_FOLDER"]
	os.makedirs(upload_folder, exist_ok=True)

	filename = secure_filename(dataset_file.filename or "uploaded_dataset.csv")
	file_path = os.path.join(upload_folder, filename)
	dataset_file.save(file_path)

	results = run_experiment(
		filepath=file_path,
		n_tasks=task_count or 100,
		algorithms=algorithms,
	)

	return render_template("results.html", results=results)
