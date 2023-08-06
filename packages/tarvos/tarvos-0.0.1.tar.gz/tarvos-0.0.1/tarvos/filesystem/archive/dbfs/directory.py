class Directory:

	KEY = 'directory'

	@staticmethod
	def initialize(self):
		pass

	def __init__(self, node=None):
		self.node = node
		self.id = None

	def __lshift__(self, file):
		raise NotImplementedError

	def __rshift__(self, path):
		raise NotImplementedError