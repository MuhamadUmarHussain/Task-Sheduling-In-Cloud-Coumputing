import pandas as pd


def load_tasks(filepath: str, n_tasks: int) -> list:
	"""Load task lengths from CSV/TXT and return the first n_tasks values."""
	lower_path = filepath.lower()

	if lower_path.endswith(".txt"):
		df = pd.read_csv(
			filepath,
			header=None,
			names=["task_length"],
			sep=r"[\s,;]+",
			engine="python",
		)
	else:
		df = pd.read_csv(filepath)
		if "task_length" not in df.columns:
			raise ValueError("Missing required column: 'task_length'")

	task_lengths = pd.to_numeric(df["task_length"], errors="coerce").dropna()
	return task_lengths.head(n_tasks).tolist()
