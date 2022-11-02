from pathlib import Path

from .subproc import run, run_fn, runs
from .config import switcher_read
from .structs import ChangeUser, Program, Programs
from .switch import switch_user, restore_user
from .options import set_options, restore_options
from .proc import kill_all, wait_process_close, wait_process_open

def valorant_start(cUser: ChangeUser):
	set_options(cUser)

	switch_user(cUser.user)

	run_fn(launch_valorant)
	wait_process_open("VALORANT.exe")
	wait_process_close("VALORANT.exe")

	restore_user()

	restore_options(cUser)

def get_programs():
	programsData = switcher_read("programs.json")
	programs = Programs([], [], [], "")
	for p in programsData:
		program = Program(Path(p["path"]), p["type"], p["beforeLaunch"], p["close"])
		programs.list.append(program)
		if (program.type == "launcher"):
			programs.launcher = program
		elif (program.beforeLaunch):
			programs.beforeLaunch.append(program)
		else:
			programs.afterLaunch.append(program)
	return programs

def launch_valorant():
	programs = get_programs()
	runs(programs.beforeLaunch)
	run(programs.launcher)
	wait_process_open("VALORANT.exe")
	runs(programs.afterLaunch)
	wait_process_close("VALORANT.exe")
	kill_all([p.path.name for p in programs.list])
