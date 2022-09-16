from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from ValConfig.structs import User

@dataclass
class ChangeUser():
	user: User
	defaultUser: str
	cfg: str
	pull: bool
	username: str = field(init=False)
	isDefault: bool = field(init=False)

	def __post_init__(self):
		if not self.user:
			return
		self.username = self.user.username
		self.isDefault = self.username == self.defaultUser

@dataclass
class Program():
	path: Path
	type: str
	beforeLaunch: bool
	close: bool

@dataclass
class Programs():
	list: List[Program]
	beforeLaunch: List[Program]
	afterLaunch: List[Program]
	launcher: Program
