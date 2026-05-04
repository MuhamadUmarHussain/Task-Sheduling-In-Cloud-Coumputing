from simulator.utils import execute_task_on_vm


def eft_schedule(tasks: list[float], vms: list, log: list[dict] | None = None) -> float:
	if not vms:
		raise ValueError("VM list cannot be empty.")

	max_finish_time = 0.0

	for task_length in tasks:
		selected_vm = min(
			vms,
			key=lambda vm: vm.available_time + (task_length / vm.mips),
		)

		finish_time = execute_task_on_vm(task_length, selected_vm, log=log)
		if finish_time > max_finish_time:
			max_finish_time = finish_time

	return max_finish_time
