from dataclasses import InitVar, dataclass, field
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