class File:

	KEY = 'file'

	@staticmethod
	def initialize(self):
		pass

	def __init__(self, data, size, node=None):
		self.data = data
		self.size = size
		self.node = node
		self.id = None

	def __lshift__(self, file):
		file.open()
		file.read()

		data = file.data
		size = len(file.data)

		try:
			self.get()
		except:
			pass

		raise NotImplementedError

	def __rshift__(self, path):
		raise NotImplementedError


	def get(self):
		pass

	def insert(self):
		pass

	def delete(self):
		pass