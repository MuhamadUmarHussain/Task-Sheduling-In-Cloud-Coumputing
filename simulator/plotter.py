from pathlib import Path

import matplotlib.pyplot as plt


def plot_results(results) -> dict[str, str]:
	"""Generate and save comparison bar charts for experiment results."""
	if isinstance(results, dict):
		rows = [results]
	else:
		rows = list(results)

	if not rows:
		raise ValueError("No results provided for plotting.")

	algorithms = [str(row.get("algorithm", f"algorithm_{index + 1}")) for index, row in enumerate(rows)]
	makespans = [float(row.get("makespan", 0.0)) for row in rows]
	utilizations = [float(row.get("utilization", 0.0)) for row in rows]
	throughputs = [float(row.get("throughput", 0.0)) for row in rows]

	graphs_dir = Path("static/graphs")
	graphs_dir.mkdir(parents=True, exist_ok=True)

	def _save_bar_chart(values: list[float], title: str, ylabel: str, filename: str) -> str:
		plt.figure(figsize=(8, 5))
		plt.bar(algorithms, values)
		plt.title(title)
		plt.xlabel("Algorithm")
		plt.ylabel(ylabel)
		plt.tight_layout()

		output_path = graphs_dir / filename
		plt.savefig(output_path)
		plt.close()
		return str(output_path).replace("\\", "/")

	return {
		"makespan_chart": _save_bar_chart(
			values=makespans,
			title="Makespan Comparison",
			ylabel="Makespan",
			filename="makespan_comparison.png",
		),
		"utilization_chart": _save_bar_chart(
			values=utilizations,
			title="Utilization Comparison",
			ylabel="Utilization",
			filename="utilization_comparison.png",
		),
		"throughput_chart": _save_bar_chart(
			values=throughputs,
			title="Throughput Comparison",
			ylabel="Throughput",
			filename="throughput_comparison.png",
		),
	}
