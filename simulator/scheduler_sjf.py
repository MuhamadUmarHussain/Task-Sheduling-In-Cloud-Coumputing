from simulator.utils import execute_task_on_vm


def sjf_schedule(tasks: list[float], vms: list) -> float:
	if not vms:
		raise ValueError("VM list cannot be empty.")

	sorted_tasks = sorted(tasks)
	max_finish_time = 0.0

	for index, task_length in enumerate(sorted_tasks):
		vm = vms[index % len(vms)]
		finish_time = execute_task_on_vm(task_length, vm)
		if finish_time > max_finish_time:
			max_finish_time = finish_time

	return max_finish_time
