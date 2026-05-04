import os

from flask import Blueprint, current_app, render_template, request, send_file, abort, Response
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
	# Accept multiple ways the form may send algorithms: as repeated
	# `algorithms` fields or as `algorithms[]` (some clients/JS use that).
	algorithms = request.form.getlist("algorithms") or request.form.getlist("algorithms[]")

	# If a single comma-separated string was submitted, split it.
	if algorithms and isinstance(algorithms, str):
		algorithms = [a.strip() for a in algorithms.split(',') if a.strip()]

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

	return render_template("results.html", results=results, dataset_filename=filename, chart_results=results)


@main.route("/download_csv")
def download_csv():
	"""Generate and return per-task CSV for a selected algorithm.

	Query params: algorithm (fcfs|sjf|eft), dataset (uploaded filename), task_count
	"""
	algorithm = request.args.get("algorithm")
	dataset = request.args.get("dataset")
	task_count = request.args.get("task_count", type=int) or 100

	if not algorithm or not dataset:
		abort(400, "Missing algorithm or dataset parameter")

	upload_folder = current_app.config["UPLOAD_FOLDER"]
	file_path = os.path.join(upload_folder, secure_filename(dataset))
	if not os.path.exists(file_path):
		abort(404, "Dataset file not found")

	# Import schedulers here to avoid circular imports
	from simulator.task_loader import load_tasks
	from simulator.datacenter import create_datacenter
	from simulator.scheduler_fcfs import fcfs_schedule
	from simulator.scheduler_sjf import sjf_schedule
	from simulator.scheduler_eft import eft_schedule

	tasks = load_tasks(file_path, task_count)
	vms = create_datacenter()
	log: list[dict] = []

	alg = algorithm.strip().lower()
	if alg == "fcfs":
		fcfs_schedule(tasks, vms, log=log)
	elif alg == "sjf":
		sjf_schedule(tasks, vms, log=log)
	elif alg == "eft":
		eft_schedule(tasks, vms, log=log)
	else:
		abort(400, "Unknown algorithm")

	# Build CSV in memory
	import io, csv

	output = io.StringIO()
	writer = csv.DictWriter(output, fieldnames=["VM", "MI", "Start", "Finish"])
	writer.writeheader()
	for entry in log:
		writer.writerow({
			"VM": entry.get("VM"),
			"MI": entry.get("MI"),
			"Start": entry.get("Start"),
			"Finish": entry.get("Finish"),
		})

	output.seek(0)
	filename = f"{algorithm}_tasks{task_count}.csv"
	return Response(
		output.getvalue(),
		mimetype="text/csv",
		headers={"Content-Disposition": f"attachment;filename={filename}"},
	)


@main.route("/plot_modal")
def plot_modal():
	algorithm = request.args.get("algorithm")
	dataset = request.args.get("dataset")
	task_count = request.args.get("task_count", type=int) or 100

	if not algorithm or not dataset:
		abort(400, "Missing algorithm or dataset parameter")

	upload_folder = current_app.config["UPLOAD_FOLDER"]
	file_path = os.path.join(upload_folder, secure_filename(dataset))
	if not os.path.exists(file_path):
		abort(404, "Dataset file not found")

	from simulator.task_loader import load_tasks
	from simulator.datacenter import create_datacenter
	from simulator.scheduler_fcfs import fcfs_schedule
	from simulator.scheduler_sjf import sjf_schedule
	from simulator.scheduler_eft import eft_schedule

	tasks = load_tasks(file_path, task_count)
	vms = create_datacenter()
	log: list[dict] = []

	alg = algorithm.strip().lower()
	if alg == "fcfs":
		fcfs_schedule(tasks, vms, log=log)
	elif alg == "sjf":
		sjf_schedule(tasks, vms, log=log)
	elif alg == "eft":
		eft_schedule(tasks, vms, log=log)
	else:
		abort(400, "Unknown algorithm")

	# Aggregate busy time per VM
	busy = {}
	makespan = 0.0
	for e in log:
		vm = e.get("VM")
		start = float(e.get("Start", 0))
		finish = float(e.get("Finish", 0))
		busy[vm] = busy.get(vm, 0.0) + (finish - start)
		if finish > makespan:
			makespan = finish

	labels = sorted(busy.keys(), key=lambda s: int(s.replace('VM', '')))
	values = [busy.get(l, 0.0) / (makespan if makespan > 0 else 1) for l in labels]

	# Render bar chart to PNG
	import io
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt

	fig, ax = plt.subplots(figsize=(8, 4.5))
	ax.bar(labels, values, color='#0d6efd')
	ax.set_ylim(0, 1.0)
	ax.set_ylabel('Util.')
	ax.set_title(f"{algorithm} n={task_count}")
	ax.grid(axis='y', linestyle='--', alpha=0.3)
	plt.tight_layout()

	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	plt.close(fig)
	buf.seek(0)
	return send_file(buf, mimetype='image/png')
