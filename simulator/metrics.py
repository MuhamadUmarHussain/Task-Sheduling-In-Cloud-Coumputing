def calculate_metrics(vms: list, total_tasks: int, finish_time: float) -> dict[str, float]:
	makespan = finish_time

	if makespan <= 0:
		return {
			"makespan": makespan,
			"utilization": 0.0,
			"throughput": 0.0,
		}

	utilization = sum(vm.available_time for vm in vms) / (len(vms) * makespan)
	throughput = total_tasks / makespan

	return {
		"makespan": makespan,
		"utilization": utilization,
		"throughput": throughput,
	}
