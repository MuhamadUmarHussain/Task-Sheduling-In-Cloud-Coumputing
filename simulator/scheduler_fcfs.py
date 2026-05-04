from simulator.utils import execute_task_on_vm


def fcfs_schedule(tasks: list[float], vms: list, log: list[dict] | None = None) -> float:
	if not vms:
		raise ValueError("VM list cannot be empty.")

	max_finish_time = 0.0
	for index, task_length in enumerate(tasks):
		vm = vms[index % len(vms)]
		finish_time = execute_task_on_vm(task_length, vm, log=log, task_id=index)
		if finish_time > max_finish_time:
			max_finish_time = finish_time

	return max_finish_time
