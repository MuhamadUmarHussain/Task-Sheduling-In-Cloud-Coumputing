def execute_task_on_vm(task_length: float, vm, log: list[dict] | None = None, task_id: int | None = None) -> float:
	"""Execute a task on a VM and return finish time.

	If `log` is provided, append a record with VM, MI, Start and Finish times.
	"""
	execution_time = task_length / vm.mips
	start_time = vm.available_time
	finish_time = start_time + execution_time
	vm.available_time = finish_time

	if log is not None:
		log.append(
			{
				"VM": f"VM{vm.id}",
				"MI": float(task_length),
				"Start": float(start_time),
				"Finish": float(finish_time),
			}
		)

	return finish_time
