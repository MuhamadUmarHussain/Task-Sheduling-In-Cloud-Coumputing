def execute_task_on_vm(task_length: float, vm) -> float:
	execution_time = task_length / vm.mips
	start_time = vm.available_time
	finish_time = start_time + execution_time
	vm.available_time = finish_time
	return finish_time
