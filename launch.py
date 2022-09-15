from .structs import ChangeUser
from .switch import switch_user, restore_user
from .options import set_options, restore_options
from .proc import wait_process_close, wait_process_open

def valorant_start(cUser: ChangeUser):
	set_options(cUser)

	switch_user(cUser.user)

	wait_process_open("VALORANT.exe")
	wait_process_close("VALORANT.exe")

	restore_user()

	restore_options(cUser)

