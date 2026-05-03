from dataclasses import dataclass


@dataclass
class VM:
	id: int
	mips: int
	ram: int
	available_time: float = 0


def create_datacenter() -> list[VM]:
	"""Create a datacenter with 10 heterogeneous virtual machines."""
	vms = [
		VM(id=1, mips=1000, ram=512),
		VM(id=2, mips=1200, ram=768),
		VM(id=3, mips=1400, ram=1024),
		VM(id=4, mips=1600, ram=1536),
		VM(id=5, mips=1800, ram=2048),
		VM(id=6, mips=2000, ram=1024),
		VM(id=7, mips=2200, ram=1536),
		VM(id=8, mips=2500, ram=2048),
		VM(id=9, mips=2900, ram=1024),
		VM(id=10, mips=3200, ram=2048),
	]
	return vms
