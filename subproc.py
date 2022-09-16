
import subprocess
from typing import List
from threading import Thread

from .structs import Program

def run_fn(fn):
	thread = Thread(target=fn)
	thread.start()

def run(program: Program ):
	thread = Thread(target=lambda: subprocess.run("", executable=program.path))
	thread.start()

def runs(programs: List[Program]):
	for p in programs:
		run(p)