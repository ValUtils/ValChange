import os
from time import sleep
import psutil

def find_procs_by_name(name):
	ls = []
	for p in psutil.process_iter(["exe"]):
		if p.info['exe'] and os.path.basename(p.info['exe']) == name:
			ls.append(p)
	return ls

def wait_process_close(name):
	ls = find_procs_by_name(name)
	psutil.wait_procs(ls)

def wait_process_open(name: str):
	while True:
		for p in psutil.process_iter(["exe"]):
			if p.info['exe'] and os.path.basename(p.info['exe']) == name:
				return True
		sleep(1)

def kill_all(nameList):
	ls = []
	for p in psutil.process_iter(["exe"]):
		if p.info['exe'] and os.path.basename(p.info['exe']) in nameList:
			p.kill()
			ls.append(p)
	psutil.wait_procs(ls)
