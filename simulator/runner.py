from simulator.datacenter import create_datacenter
from simulator.metrics import calculate_metrics
from simulator.plotter import plot_results
from simulator.results_saver import save_results
from simulator.scheduler_eft import eft_schedule
from simulator.scheduler_fcfs import fcfs_schedule
from simulator.scheduler_sjf import sjf_schedule
from simulator.task_loader import load_tasks


def _build_vm_data(vms: list) -> list[dict[str, float | str]]:
	makespan = max((vm.available_time for vm in vms), default=0.0)
	if makespan <= 0:
		return [{"name": f"VM{vm.id}", "utilization": 0.0} for vm in vms]

	return [
		{
			"name": f"VM{vm.id}",
			"utilization": round(vm.available_time / makespan, 4),
		}
		for vm in vms
	]


def run_experiment(filepath: str, n_tasks: int, algorithms: list[str]) -> list[dict[str, float | str]]:
	"""Run selected scheduling algorithms and return UI-ready result rows."""
	if n_tasks <= 0:
		raise ValueError("n_tasks must be greater than 0.")

	tasks = load_tasks(filepath, n_tasks)

	algorithm_map = {
		"fcfs": ("FCFS", fcfs_schedule),
		"sjf": ("SJF", sjf_schedule),
		"eft": ("EFT", eft_schedule),
	}

	selected = algorithms or ["fcfs", "sjf", "eft"]
	results: list[dict[str, float | str]] = []

	for algorithm_key in selected:
		normalized = algorithm_key.strip().lower()
		if normalized not in algorithm_map:
			continue

		algorithm_name, scheduler_fn = algorithm_map[normalized]
		vms = create_datacenter()
		finish_time = scheduler_fn(tasks, vms)
		metrics = calculate_metrics(vms, total_tasks=len(tasks), finish_time=finish_time)
		results.append({"algorithm": algorithm_name, "tasks": len(tasks), "vm_data": _build_vm_data(vms), **metrics})

	if not results:
		raise ValueError("No valid algorithms selected.")

	save_results(results, task_count=len(tasks))
	plot_results(results)

	return results
