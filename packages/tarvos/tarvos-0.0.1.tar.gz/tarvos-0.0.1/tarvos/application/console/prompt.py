class TYPE:

	# OK / CANCEL

	# YES / NO

	# <string>

	# <int>

	# <number>

	# <email>?

	# <password>?

	# One from [OPT-1, OPT-2, OPT-3, ...]
	# Many from [OPT-1, OPT-2, OPT-3, ...]
	pass


class Option:

	def __init__(self, ob, default=False):
		self.ob = ob


class Prompt:

	def __init__(self):
		# Settings
		self.type = 'class' or []
		self.message = 'string' or []
		self.validation = 'function'
		self.limit = 'int'

		# Activity
		self.attempts = 0


	def prompt(self):
		pass