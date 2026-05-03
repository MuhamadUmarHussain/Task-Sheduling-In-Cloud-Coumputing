import csv
from datetime import datetime
from pathlib import Path


def save_results(results, task_count: int) -> str:
	"""Append experiment results to CSV and return the output file path."""
	output_path = Path("data/results/experiment_results.csv")
	output_path.parent.mkdir(parents=True, exist_ok=True)

	fieldnames = [
		"timestamp",
		"tasks",
		"algorithm",
		"makespan",
		"utilization",
		"throughput",
	]

	if isinstance(results, dict):
		rows = [results]
	else:
		rows = list(results)

	file_exists = output_path.exists()
	timestamp = datetime.now().isoformat(timespec="seconds")

	with output_path.open("a", newline="", encoding="utf-8") as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		if not file_exists:
			writer.writeheader()

		for result in rows:
			writer.writerow(
				{
					"timestamp": timestamp,
					"tasks": task_count,
					"algorithm": result.get("algorithm", "unknown"),
					"makespan": result.get("makespan", 0),
					"utilization": result.get("utilization", 0),
					"throughput": result.get("throughput", 0),
				}
			)

	return str(output_path)
