import pandas as pd
import zipfile
import tempfile
from pathlib import Path


def _read_csv_with_task_length(path: str) -> pd.Series:
	df = pd.read_csv(path)
	if "task_length" not in df.columns:
		raise ValueError("Missing required column: 'task_length'")
	return pd.to_numeric(df["task_length"], errors="coerce").dropna()


def _read_txt(path: str) -> pd.Series:
	# Supports whitespace, comma, or semicolon separated numeric values
	df = pd.read_csv(path, header=None, names=["task_length"], sep=r"[\s,;]+", engine="python")
	return pd.to_numeric(df["task_length"], errors="coerce").dropna()


def load_tasks(filepath: str, n_tasks: int) -> list:
	"""Load task lengths from CSV, TXT, or ZIP (containing CSV/TXT) and return the first n_tasks values."""
	lower_path = filepath.lower()

	if lower_path.endswith(".zip"):
		with zipfile.ZipFile(filepath) as z:
			candidates = [name for name in z.namelist() if name.lower().endswith((".csv", ".txt"))]
			if not candidates:
				raise ValueError("ZIP archive contains no CSV or TXT files")
			# choose the first matching file
			target = candidates[0]
			with tempfile.TemporaryDirectory() as td:
				z.extract(target, path=td)
				inner_path = Path(td) / target
				inner_path_str = str(inner_path)
				if inner_path_str.lower().endswith(".txt"):
					series = _read_txt(inner_path_str)
				else:
					series = _read_csv_with_task_length(inner_path_str)
	elif lower_path.endswith(".txt"):
		series = _read_txt(filepath)
	else:
		series = _read_csv_with_task_length(filepath)

	return series.head(n_tasks).tolist()
